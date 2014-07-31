from django.template import Library
from django.core.exceptions import ObjectDoesNotExist
from site_core.models import Parameter
import json

register = Library()


@register.assignment_tag
def html_from_parameters(name):
    try:
        parameter = Parameter.objects.get(name=name)
        if parameter.enable:
            return parameter.value
        else:
            return ''
    except ObjectDoesNotExist:
        return ''


