'''Formularios que heredan de ``django.forms.Form``
'''

from collections import OrderedDict
from typing import Any, Dict

from django.core.cache import cache
from django import forms

from .registries import modules


class DynamicForm(forms.Form):
    '''
    Formulario cuyos campos se generan de forma dinámica de acuerdo a una
    estructura en formato json que se obtiene de la base de datos. Para obtener
    esta estructura, esta clase recibe un kwarg ``structure`` que es una
    instancia de ``forge.models.Structure``
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Extraer el parámetro `structure de los argumentos` antes de ejecutar
        # el método `init` de la clase padre
        structure = kwargs.pop('structure')

        super().__init__(*args, **kwargs)

        fields = structure.structure['fields']
        self.structure_id = structure.id

        # Primero consultar la cache
        self.fields = cache.get(f'fields_{self.structure_id}')

        if not self.fields:
            self.fields = OrderedDict(
                (field['name'], generate_field(dict(field))) for field in fields)
            cache.set(f'fields_{self.structure_id}', self.fields)


def generate_field(field: Dict[str, str]) -> forms.Field:  # pylint: disable=too-many-branches,too-many-return-statements

    field_classes = {
        'text': forms.CharField,
        'textarea': forms.CharField,
        'email': forms.EmailField,
        'radio': forms.ChoiceField,
        'select': forms.ChoiceField,
        'multiselect': forms.MultipleChoiceField,
        'date': forms.DateField,
        'datetime': forms.DateTimeField,
        'duration': forms.DurationField,
        'time': forms.TimeField,
        'integer': forms.IntegerField,
        'decimal': forms.DecimalField,
        'file': forms.FileField,
        'filepath': forms.FilePathField,
        'image': forms.ImageField,
        'checkbox': forms.BooleanField
    }

    custom_widgets = {
        'textarea': forms.Textarea(),
        'radio': forms.RadioSelect(),
        'date': forms.SelectDateWidget(attrs={'type': 'date'}),
        'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'time': forms.TimeInput(attrs={'type': 'time'}),
        'checkbox': forms.CheckboxInput(),
    }

    try:
        field_type = field['type']
    except KeyError:
        raise ValueError('Wrong or not implemented field type')

    field_class = None
    registred_widget = None

    for module in modules.values():
        try:
            field_class = module.fields[field_type]['field_type']
        except KeyError:
            continue
        else:
            registred_widget = module.fields[field_type]['widget']

    if not field_class:
        try:
            field_class = field_classes[field_type]
        except KeyError:
            raise ValueError('Wrong or not implemented field type')

    field_options = field.get('options', {})
    field_widget = registred_widget or custom_widgets.get(field_type, None)

    return field_class(widget=field_widget, **field_options)
