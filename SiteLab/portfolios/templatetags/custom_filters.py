from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    """
    Allows template to get a form field by its name string: 
    {{ form|get_field:'field_name' }}
    """
    try:
        return form[field_name]
    except KeyError:
        return None

@register.filter
def add(value, arg):
    """Adds the arg to the value."""
    return str(value) + str(arg)