'''
Validaciones
'''
from copy import deepcopy
from typing import Dict, List

from django.core.exceptions import ValidationError
from jsonschema import Draft4Validator

# Missing properties:
# - widget
# - error_messages

BASE_FIELD = {
    'type': 'object',
    'properties': {
        'type': {'enum': []},
        'name': {'type': 'string'},
        'options': {
            'type': 'object',
            'properties': {
                'label': {'type': 'string', 'minLength': 1},
                'label_suffix': {'type': 'string', 'minLength': 1},
                'initial': {},
                'required': {'type': 'boolean'},
                'help_text': {'type': 'string'},
                'validators': {'type': 'array', 'items': {'type': 'string'}},
                'disabled': {'type': 'boolean'},
            },
            'additionalProperties': False
        }
    },
    'additionalProperties': False,
    'required': ['type', 'name']
}

#################
#  TEXT FIELDS  #
#################

TEXT = deepcopy(BASE_FIELD)
TEXT['properties']['type']['enum'].append('text')  # type: ignore
TEXT['properties']['options']['properties']['strip'] = {'type': 'boolean'}  # type: ignore
TEXT['properties']['options']['properties']['max_length'] = {'type': 'integer'}  # type: ignore
TEXT['properties']['options']['properties']['min_length'] = {'type': 'integer'}  # type: ignore

TEXTAREA = deepcopy(BASE_FIELD)
TEXTAREA['properties']['type']['enum'].append('textarea')  # type: ignore
TEXTAREA['properties']['options']['properties']['strip'] = {'type': 'boolean'}  # type: ignore
TEXTAREA['properties']['options']['properties']['max_length'] = {'type': 'integer'}  # type: ignore
TEXTAREA['properties']['options']['properties']['min_length'] = {'type': 'integer'}  # type: ignore

EMAIL = deepcopy(BASE_FIELD)
EMAIL['properties']['type']['enum'].append('email')  # type: ignore
EMAIL['properties']['options']['properties']['max_length'] = {'type': 'integer'}  # type: ignore
EMAIL['properties']['options']['properties']['min_length'] = {'type': 'integer'}  # type: ignore

###################
#  CHOICE FIELDS  #
###################

RADIO = deepcopy(BASE_FIELD)
RADIO['properties']['type']['enum'].append('radio')  # type: ignore
RADIO['properties']['options']['properties']['choices'] = {  # type: ignore
    'type': 'array',
    'items': {
        'type': 'array',
        'minItems': 2,
        'maxItems': 2,
        'items': {}
    }
}


SELECT = deepcopy(RADIO)
SELECT['properties']['type']['enum'][0] = 'select'  # type: ignore

MULTISELECT = deepcopy(RADIO)
MULTISELECT['properties']['type']['enum'][0] = 'multiselect'  # type: ignore

##########################
#  DATE AND TIME FIELDS  #
##########################
# Missing properties:
# - input_formats
DATE = deepcopy(BASE_FIELD)
DATE['properties']['type']['enum'].append('date')  # type: ignore

# Missing properties:
# - input_formats
DATETIME = deepcopy(BASE_FIELD)
DATETIME['properties']['type']['enum'].append('datetime')  # type: ignore

DURATION = deepcopy(BASE_FIELD)
DURATION['properties']['type']['enum'].append('duration')  # type: ignore

# Missing properties:
# - input_formats
TIME = deepcopy(BASE_FIELD)
TIME['properties']['type']['enum'].append('time')  # type: ignore

####################
#  NUMERIC FIELDS  #
####################

INTEGER = deepcopy(BASE_FIELD)
INTEGER['properties']['type']['enum'].append('integer')  # type: ignore
INTEGER['properties']['options']['properties']['max_value'] = {'type': 'integer'}  # type: ignore
INTEGER['properties']['options']['properties']['min_value'] = {'type': 'integer'}  # type: ignore

DECIMAL = deepcopy(BASE_FIELD)
DECIMAL['properties']['type']['enum'].append('decimal')  # type: ignore
DECIMAL['properties']['options']['properties']['max_value'] = {'type': 'number'}  # type: ignore
DECIMAL['properties']['options']['properties']['min_value'] = {'type': 'number'}  # type: ignore

#################
#  FILE FIELDS  #
#################

FILE = deepcopy(BASE_FIELD)
FILE['properties']['type']['enum'].append('file')  # type: ignore
FILE['properties']['options']['properties']['max_length'] = {'type': 'number'}  # type: ignore
FILE['properties']['options']['properties']['allow_empty_file'] = {'type': 'boolean'}  # type: ignore

FILEPATH = deepcopy(BASE_FIELD)
FILEPATH['properties']['type']['enum'].append('filepath')  # type: ignore
FILEPATH['properties']['options']['properties']['path'] = {'type': 'string'}  # type: ignore
FILEPATH['properties']['options']['properties']['recursive'] = {'type': 'boolean'}  # type: ignore
FILEPATH['properties']['options']['properties']['match'] = {'type': 'string'}  # type: ignore
FILEPATH['properties']['options']['properties']['allow_files'] = {'type': 'boolean'}  # type: ignore
FILEPATH['properties']['options']['properties']['allow_folders'] = {'type': 'boolean'}  # type: ignore

IMAGE = deepcopy(BASE_FIELD)
IMAGE['properties']['type']['enum'].append('image')  # type: ignore

####################
#  BOOLEAN FIELDS  #
####################

CHECKBOX = deepcopy(BASE_FIELD)
CHECKBOX['properties']['type']['enum'].append('checkbox')  # type: ignore

##################
#  FINAL SCHEMA  #
##################

ALL_FIELDS = [TEXT, TEXTAREA, EMAIL, RADIO, SELECT, MULTISELECT, DATE, DATETIME,
              DURATION, TIME, INTEGER, DECIMAL, FILE, FILEPATH, IMAGE, CHECKBOX, ]
SCHEMA = {
    'id': 'http://forge.hab.desoft.cu#',
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'schema for a form',
    'type': 'object',
    'properties': {
        'fields': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'anyOf': ALL_FIELDS
            }
        }
    },
    'required': ['fields'],
}


def validate_structure(structure: Dict) -> None:

    validator = Draft4Validator(SCHEMA)
    errors = list(validator.iter_errors(structure))

    if errors:
        messages: List
        if len(errors) > 1:
            messages = list(set(context.message for error in errors for context in error.context))
            valid_messages = [message for message in messages if not 'is not one of' in message]
            if len(messages) != len(valid_messages):
                valid_messages.append('Incorrect type of field')
        else:
            valid_messages = [errors[0].message]

        raise ValidationError([ValidationError(message) for message in sorted(valid_messages)])
