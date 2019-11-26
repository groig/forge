import pytest

from django.core.exceptions import ValidationError

from forge.validation import validate_structure
from .fixtures import FULL_STRUCTURE_VALID, SELECT_CHOICES


VALID_STRUCTURES = [{'fields': [field]} for field in FULL_STRUCTURE_VALID['fields']]

VALID_STRUCTURES.append(FULL_STRUCTURE_VALID)


@pytest.mark.parametrize('structure', VALID_STRUCTURES)
def test_validate_structure_valid(structure):
    validate_structure(structure)


EMPTY_STRUCTURE = {}
EMPTY_FIELDS = {'fields': []}

FULL_STRUCTURE_INVALID = {'fields': [
    {'namex': 'first_name', 'type': 'text', 'options': {'required': True, 'max_length': 25}},
    {'name': 'first_name', 'types': 'text', 'options': {'required': True, 'max_length': 25}},
    {'name': 'first_name', 'type': 'text', 'options': {'requireded': True, 'max_length': 25}},
    {'name': 'smallcv', 'type': 'textarea', 'extra': 'NOT ALLOWED', 'options': {
        'label': 'Small CV', 'help_text': 'Please insert a small CV'}},
    {'name': 'e-mail', 'type': 'email', 'options': {'required': True, 'min_length': 5, 'extra': 'NOT ALLOWED'}},
    {'name': 'marital_status', 'type': 'radio', 'options': {'label': 'Marital Status', 'choices': [
        ['single', 'Single'], ['married', 'Married'], ['divorced', 'Divorced'], ['Widower']]}},
    {'name': 'occupation', 'type': 'select', 'options': {'asdasd'}},
    {'name': 'occupation_multiselect', 'type': 'multiselectis', 'options': {'choices': SELECT_CHOICES}},
    {'namex': 'date', 'type': 'date'},
    {'name': 'datetime', 'type': 'datetimes'},
    {'name': 'duration', 'type': 'durations'},
    {'name': 'time', 'type': 'times'},
    {'name': 'integer', 'type': 'integer', 'options': {'ma_value': 10, 'min_value': 5}},
    {'name': 'integer', 'type': 'integer', 'options': {'max_value': 'asdasd', 'min_value': 5}},
    {'name': 'decimal', 'type': 'decimall', 'options': {'max_value': 10.1, 'min_value': 5.1}},
    {'name': 'filepath', 'type': 'filepat', 'options': {'path': 1, 'required': False, 'allow_files': True}},
    {'name': 'image', 'type': 'images', 'options': {'required': False}},
    {'name': 'internet', 'type': 'checkboxx'}
]}

INVALID_STRUCTURES = [{'fields': [field]} for field in FULL_STRUCTURE_INVALID['fields']]

INVALID_STRUCTURES.extend([FULL_STRUCTURE_INVALID, EMPTY_STRUCTURE, EMPTY_FIELDS])


@pytest.mark.parametrize('structure', INVALID_STRUCTURES)
def test_validate_structure_invalid(structure):
    with pytest.raises(ValidationError):
        validate_structure(structure)
