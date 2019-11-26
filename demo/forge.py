from django import forms

from forge.registries import modules, Module

module = Module('A demo module')


class CustomFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = 'ESTEESUNCAMPOREGISTRDOOOOO'

module.register_field('first_custom_field', CustomFormField)

modules.register(module)
