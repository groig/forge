'''
Vistas de la aplicación.
'''
# pylint: disable=too-many-ancestors
from copy import deepcopy
from typing import Any
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction, DatabaseError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from .decorators import cache_page
from .forms import DynamicForm
from .models import Data, Structure
from .utils import (acquire_lock, release_lock,
                    ResourceAlreadyBlocked, UserDoesNotOwnTheLock)

#############################
#  Structure-related views  #
#############################


@login_required
@cache_page(60 * 60)
def preview_structure(request: HttpRequest, slug: str, pk: UUID) -> HttpResponse:  # pylint: disable=unused-argument, invalid-name
    '''
    Vista para renderizar una estructura de formulario sin
    controles para hacerle submit.
    '''
    structure = Structure.objects.get(pk=pk)
    form = DynamicForm(structure=structure)
    return render(request, 'forge/form.html',
                  {'form': form, 'object': structure, 'is_structure': True, 'is_preview': True})


class StructureCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    '''
    Vista para crear instancias de ``forge.models.Structure``
    '''
    model = Structure
    fields = ('name', 'module', 'structure',)
    success_message = 'Estructura creada correctamente.'
    error_message = 'La validación de la estructura falló. Revise los campos marcados'

    def form_valid(self, form: DynamicForm) -> bool:
        # Este método se sobreescribe para adicionar el dato del usuario que
        # crea la estructura al formulario antes de guardarlo
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form: DynamicForm) -> bool:
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class StructureUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
    Vista para actualizar los datos de una instancia de
    ``forge.models.Structure``
    '''
    model = Structure
    fields = ('name', 'module', 'structure',)
    success_message = 'Estructura actualizada correctamente.'
    warning_message = 'La estructura ha cambiado. Es posible que las instancias no se renderizen correctamente'

    def form_valid(self, form: DynamicForm) -> bool:
        if self.object.data_set.count():
            messages.warning(self.request, self.warning_message)
        return super().form_valid(form)


class StructureDetails(LoginRequiredMixin, DetailView):
    '''
    Vista para mostrar los detalles de una instancia de
    ``forge.models.Structure``
    '''
    model = Structure


class StructureList(LoginRequiredMixin, ListView):
    '''
    Vista para mostrar todas las instancias de ``forge.models.Structure``
    '''
    model = Structure
    template_name = 'forge/index.html'


class StructureDelete(UserPassesTestMixin, DeleteView):
    '''
    Vista para eliminar una instancia de ``forge.models.Structure``
    '''
    model = Structure
    success_url = reverse_lazy('forge:index')
    success_message = 'Estructura eliminada con éxito.'
    warning_message = 'Han quedado instancias huérfanas y ya no son accesibles desde la interfaz'

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().data_set.count():
            messages.warning(request, self.warning_message)
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self) -> bool:
        return self.request.user.is_superuser


########################
#  Data-related views  #
########################

class DataCreate(LoginRequiredMixin, View):
    form_class = DynamicForm
    structure: Structure
    success_message = 'Los datos se han guardado correctamente.'
    error_message = 'Error validando el formulario. Revise los campos marcados'

    def dispatch(self, request: HttpRequest, slug: str, pk: UUID, *args: Any, **kwargs: Any) -> HttpResponse:  # pylint: disable=arguments-differ, unused-argument
        self.structure = Structure.objects.get(pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(structure=self.structure)
        return render(request, 'forge/form.html',
                      {'form': form, 'object': self.structure, 'is_new': True})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, structure=self.structure)
        if form.is_valid():
            data = Data.objects.create(created_by=request.user, structure_id=self.structure.id,
                                       data=form.cleaned_data)
            try:
                data.save()
            except DatabaseError as error:
                self.error_message = error
            else:
                messages.success(request, self.success_message)
                return redirect(data.get_absolute_url())
        messages.error(request, self.error_message)
        return render(request, 'forge/form.html',
                      {'form': form, 'object': self.structure,
                       'is_new': True, 'is_structure': True})  # Technically we are still on a structure page


class DataUpdate(LoginRequiredMixin, View):
    '''
    Vista para actualizar una instancia de ``forge.models.Data``
    '''
    form_class = DynamicForm
    data_object: Data
    resource_locked: Data
    amend: bool
    success_message = 'Los datos se han actualizado correctamente.'
    error_message = 'Error validando el formulario. Revise los campos marcados'

    def dispatch(self, request: HttpRequest, slug: str, pk: UUID, *args: Any, **kwargs: Any) -> HttpResponse:  # pylint: disable=arguments-differ, unused-argument
        self.data_object = get_object_or_404(Data, id=pk)
        self.amend = bool(request.GET.get('amend', False))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            acquire_lock(request.user, self.data_object)
        except ResourceAlreadyBlocked as info:
            messages.info(request, info)
            return redirect(self.data_object.get_absolute_url())
        form = self.form_class(data=self.data_object.data, structure=self.data_object.structure)
        return render(request, 'forge/form.html',
                      {'form': form, 'object': self.data_object})

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            with transaction.atomic():
                form = self.form_class(data=request.POST, structure=self.data_object.structure)
                if form.is_valid():
                    self.resource_locked = deepcopy(self.data_object)
                    self.data_object.data = form.cleaned_data
                    if self.amend:
                        amended_data = Data(created_by=request.user, structure=self.data_object.structure,
                                            data=self.data_object.data, parent=self.data_object)
                        self.data_object = amended_data
                    try:
                        self.data_object.save()
                    except DatabaseError as error:
                        self.error_message = error
                    else:
                        release_lock(request.user, self.resource_locked)
                        self.success_message = 'Se ha creado una nueva instancia con los datos actualizados.'
                        messages.success(request, self.success_message)
                        return redirect(self.data_object.get_absolute_url())
        except UserDoesNotOwnTheLock as error:
            messages.error(request, error)
            return redirect(self.resource_locked.get_absolute_url())

        messages.error(request, self.error_message)
        return render(request, 'forge/form.html',
                      {'form': form, 'object': self.data_object})


class DataDetails(LoginRequiredMixin, DetailView):
    '''
    Vista para mostrar los detalles de una instancia de ``forge.models.Data``
    '''
    model = Data


class DataDelete(UserPassesTestMixin, DeleteView):
    '''
    Vista para eliminar una instancia de ``forge.models.Data``
    '''
    model = Data
    success_message = 'La instancia se ha eliminado correctamente.'
    warning_message = 'Han quedado instancias huérfanas. Esto puede provocar problemas en el futuro.'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data_object = self.get_object()
        try:
            acquire_lock(request.user, data_object)
        except ResourceAlreadyBlocked as info:
            messages.info(request, info)
            return redirect(data_object.get_absolute_url())
        return super().get(request, args, kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            with transaction.atomic():
                data_object = self.get_object()
                children = data_object.get_children()
                delete_result = super().delete(request, *args, **kwargs)
                release_lock(request.user, data_object)
                messages.success(request, self.success_message)
                if children:
                    messages.warning(request, self.warning_message)
                return delete_result
        except UserDoesNotOwnTheLock as error:
            messages.error(request, error)
            return redirect(self.get_object().get_absolute_url())

    def get_success_url(self) -> str:
        return self.get_object().structure.get_absolute_url()

    def test_func(self) -> bool:
        return self.request.user.is_superuser
