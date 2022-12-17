from django import template
from django.db.models import Q
register = template.Library()


@register.filter
def is_equal(a, b):
    return a == b
