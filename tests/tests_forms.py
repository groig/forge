import uuid

import pytest

from django import forms
from django.core.cache import cache

from forge.forms import generate_field, DynamicForm

from .fixtures import FULL_STRUCTURE_VALID, SELECT_CHOICES


def test_generate_field_invalid():
    FIELD = {'name': 'first_name', 'type': 'nonexistent', 'options': {  # pylint: disable=invalid-name
        'required': True, 'max_length': 25}}
    with pytest.raises(ValueError):
        generate_field(FIELD)


def test_generate_field_text():
    FIELD = {'name': 'first_name', 'type': 'text', 'options': {  # pylint: disable=invalid-name
        'required': True, 'max_length': 25}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.CharField)
    assert field.max_length == 25
    assert field.required


def test_generate_field_textarea():
    FIELD = {'name': 'smallcv', 'type': 'textarea', 'options': {  # pylint: disable=invalid-name
        'label': 'Small CV', 'help_text': 'Please insert a small CV'}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.CharField)
    assert isinstance(field.widget, forms.Textarea)


def test_generate_field_email():
    FIELD = {'name': 'e-mail', 'type': 'email',  # pylint: disable=invalid-name
             'options': {'required': True, 'min_length': 5}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.EmailField)


def test_generate_field_radio():
    FIELD = {'name': 'marital_status', 'type': 'radio', 'options': {'label': 'Marital Status', 'choices': [  # pylint: disable=invalid-name
        ['single', 'Single'], ['married', 'Married'], ['divorced', 'Divorced'], ['widower', 'Widower']]}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.ChoiceField)
    assert isinstance(field.widget, forms.RadioSelect)


def test_generate_field_select():
    FIELD = {'name': 'occupation', 'type': 'select', 'options': {  # pylint: disable=invalid-name
        'choices': SELECT_CHOICES}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.ChoiceField)


def test_generate_field_multiselect():
    FIELD = {'name': 'occupation_multiselect', 'type': 'multiselect',  # pylint: disable=invalid-name
             'options': {'choices': SELECT_CHOICES}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.MultipleChoiceField)


def test_generate_field_date():
    FIELD = {'name': 'date', 'type': 'date'}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.DateField)
    assert isinstance(field.widget, forms.SelectDateWidget)


def test_generate_field_datetime():
    FIELD = {'name': 'datetime', 'type': 'datetime'}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.DateTimeField)
    assert isinstance(field.widget, forms.DateTimeInput)


def test_generate_field_duration():
    FIELD = {'name': 'duration', 'type': 'duration'}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.DurationField)


def test_generate_field_time():
    FIELD = {'name': 'time', 'type': 'time'}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.TimeField)
    assert isinstance(field.widget, forms.TimeInput)


def test_generate_field_integer():
    FIELD = {'name': 'integer', 'type': 'integer', 'options': {  # pylint: disable=invalid-name
        'max_value': 10, 'min_value': 5}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.IntegerField)


def test_generate_field_decimal():
    FIELD = {'name': 'decimal', 'type': 'decimal', 'options': {  # pylint: disable=invalid-name
        'max_value': 10.1, 'min_value': 5.1}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.DecimalField)


def test_generate_field_file():
    FIELD = {'name': 'file', 'type': 'file', 'options': {  # pylint: disable=invalid-name
        'required': False, 'allow_empty_file': True}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.FileField)


def test_generate_field_filepath():
    FIELD = {'name': 'filepath', 'type': 'filepath', 'options': {  # pylint: disable=invalid-name
        'path': '/home/roig', 'required': False, 'allow_files': True}}
    field = generate_field(FIELD)
    assert isinstance(field, forms.FilePathField)


def test_generate_field_image():
    FIELD = {'name': 'image', 'type': 'image', 'options': {'required': False}}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.ImageField)


def test_generate_field_checkbox():
    FIELD = {'name': 'internet', 'type': 'checkbox'}  # pylint: disable=invalid-name
    field = generate_field(FIELD)
    assert isinstance(field, forms.BooleanField)
    assert isinstance(field.widget, forms.CheckboxInput)


def test_dynamic_form():
    class FakeStructure():  # pylint: disable=too-few-public-methods
        def __init__(self, id, structure):  # pylint: disable=redefined-builtin
            self.id = id  # pylint: disable=invalid-name
            self.structure = structure

    structure_id = uuid.uuid4()
    structure = FakeStructure(structure_id, FULL_STRUCTURE_VALID)

    form = DynamicForm(structure=structure)

    for field in structure.structure['fields']:
        assert field['name'] in form.fields

    assert cache.get(f'fields_{structure_id}')

    cache.delete_pattern(f'fields_{structure_id}')
