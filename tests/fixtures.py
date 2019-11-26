SELECT_CHOICES = [
    ['farmer', 'Farmer'],
    ['engineer', 'Engineer'],
    ['teacher', 'Teacher'],
    ['office_clerk', 'Office Clerk'],
    ['merchant', 'Merchant'],
    ['unemployed', 'Unemployed'],
    ['retired', 'Retired'],
    ['other', 'Other'],
]

FULL_STRUCTURE_VALID = {'fields': [
    {'name': 'first_name', 'type': 'text', 'options': {'required': True, 'max_length': 25}},
    {'name': 'smallcv', 'type': 'textarea', 'options': {'label': 'Small CV', 'help_text': 'Please insert a small CV'}},
    {'name': 'e-mail', 'type': 'email', 'options': {'required': True, 'min_length': 5}},
    {'name': 'marital_status', 'type': 'radio', 'options': {'label': 'Marital Status', 'choices': [
        ['single', 'Single'], ['married', 'Married'], ['divorced', 'Divorced'], ['widower', 'Widower']]}},
    {'name': 'occupation', 'type': 'select', 'options': {'choices': SELECT_CHOICES}},
    {'name': 'occupation_multiselect', 'type': 'multiselect', 'options': {'choices': SELECT_CHOICES}},
    {'name': 'date', 'type': 'date'},
    {'name': 'datetime', 'type': 'datetime'},
    {'name': 'duration', 'type': 'duration'},
    {'name': 'time', 'type': 'time'},
    {'name': 'integer', 'type': 'integer', 'options': {'max_value': 10, 'min_value': 5}},
    {'name': 'decimal', 'type': 'decimal', 'options': {'max_value': 10.1, 'min_value': 5.1}},
    {'name': 'file', 'type': 'file', 'options': {'required': False, 'allow_empty_file': True}},
    {'name': 'filepath', 'type': 'filepath', 'options': {'path': '/home/roig', 'required': False, 'allow_files': True}},
    {'name': 'image', 'type': 'image', 'options': {'required': False}},
    {'name': 'internet', 'type': 'checkbox'}
]}
