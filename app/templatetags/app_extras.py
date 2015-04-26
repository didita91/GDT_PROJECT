from django import template
from django.templatetags.app_extras import *
from django.contrib.admin.templatetags.app_extras import * 
from django.contrib.staticfiles.templatetags.app_extras import *
register = template.Library()

@register.filter(name='display')

def display(value):
    if value == 1:
        return 'Pendiente'
    elif value == 2:
        return 'Modificado'
    elif value == 3:
        return 'Revisado'
    return ''

