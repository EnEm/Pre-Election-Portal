from django import template
import datetime

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def secondssince(value):
    return int(datetime.datetime.now().timestamp()) - int(value.timestamp())
