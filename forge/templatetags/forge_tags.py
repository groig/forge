'''
Etiquetas adicionales para las plantillas
'''
import re

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context: template.Context, url: str, slug: str=None, obj_id: str=None) -> str:  # pylint: disable=bad-whitespace
    '''
    Etiqueta para adicionar la clase css ``active`` a una etiqueta html. Útil para
    usar en un menù o barra de navegación. Determina si la url actual corresponde
    a la url pasada por parámetro.

    Uso:

    .. code-block:: html

        <li><a {% active_url url %}>Entrada</a></li>
        <li><a {% active_url url id %}>Entrada</a></li>

    '''
    try:
        if obj_id:
            pattern = '^%s$' % reverse(url, kwargs={'pk': obj_id, 'slug': slug})
        else:
            pattern = '^%s$' % reverse(url)
    except NoReverseMatch:
        pattern = url

    path = context['request'].path
    return mark_safe('class="active"') if re.search(pattern, path) else ''
