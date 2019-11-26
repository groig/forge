'''
Modelos que heredan de `django.db.models.Model`
'''
import uuid
from typing import Any, Dict

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from .registries import modules
from .validation import validate_structure


class BaseModel(models.Model):
    '''
    Modelo que sirve de base para el resto. Implementa algunos campos comunes
    así como sobreescribe el método ``save`` de ``django.db.models.Model`` para que
    el modelo se valide cada vez que se salve.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # pylint: disable=invalid-name
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=arguments-differ
        # Valida el modelo cada vez que se salve
        self.full_clean()
        super().save(*args, **kwargs)  # Llamar al método ``save`` real

    class Meta:
        abstract = True


def default_structure() -> Dict[str, list]:
    return {'fields': []}


MODULES_CHOICES = [(module_name, module_name) for module_name in modules]


class Structure(BaseModel):
    '''
    Modelo que representa la estructura de un formulario, principalmente los
    campos de los que está compuesto.

    La estructura se almacena en un campo de tipo ``jsonb`` en la base de datos.
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    module = models.CharField(max_length=255, blank=True, null=True, choices=MODULES_CHOICES)
    structure = JSONField(default=default_structure, validators=[validate_structure])

    def save(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=arguments-differ
        # Valida el modelo cada vez que se salve
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Llamar al método ``save`` real

    def get_absolute_url(self) -> str:
        return reverse('forge:structure_details',
                       kwargs={'slug': self.slug, 'pk': str(self.pk)})


class DataManager(TreeManager):
    def orphans(self) -> models.QuerySet:
        return super().get_queryset().filter(level__gt=0, parent=None)

    def structureless(self) -> models.QuerySet:
        return super().get_queryset().filter(structure=None)


class Data(BaseModel, MPTTModel):
    '''
    Modelo que representa los datos de un formulario. Está vinculado con una
    estructura mediante el campo ``structure``.

    Los datos se almacenan en un campo de tipo ``jsonb`` en la base de datos.
    '''
    structure = models.ForeignKey(Structure, null=True, blank=True,
                                  default=None, on_delete=models.SET_DEFAULT)
    data = JSONField(default=dict, encoder=DjangoJSONEncoder)
    parent = TreeForeignKey('self', null=True, blank=True, default=None,
                            on_delete=models.SET_DEFAULT, related_name='children', db_index=True)
    objects = DataManager()

    def get_absolute_url(self) -> str:
        return reverse('forge:data_details',
                       kwargs={'slug': self.structure.slug, 'pk': str(self.pk)})
