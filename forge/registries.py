from collections import OrderedDict

from django import forms


class Module:  # pylint: disable=too-few-public-methods
    def __init__(self, name):
        if not name:
            raise ValueError('El nombre del módulo no puede estar vacío')
        self.name = name
        self.fields = {}

    def register_field(self, field_name, field_type, widget=None):

        if not field_name:
            raise ValueError('El nombre del campo no puede estar vacío')
        if not issubclass(field_type, forms.Field):
            raise TypeError('El campo a registrar debe ser una subclase de django.forms.Field')
        if widget and not issubclass(widget, forms.Widget):
            raise TypeError('El widget debe ser una subclase de django.forms.Widget')

        new_field = {
            'field_type': field_type,
            'widget': widget
        }

        self.fields[field_name] = new_field


class Registry(OrderedDict):
    look_into = 'forge'

    def autodiscover(self, apps):
        for app in apps:
            try:
                package = f'{app}.{self.look_into}'.format(app, self.look_into)
                module = __import__(package)  # pylint: disable=unused-variable
            except ImportError:
                pass

    def register(self, data):
        self[data.name] = data


modules = Registry()
