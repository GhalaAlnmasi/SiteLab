from django import template

register = template.Library()


@register.filter
def field_or_template(portfolio, field_name):
    """
    Get field value with fallback to template defaults.
    Example:
        {{ portfolio|field_or_template:"about" }}
    """
    return portfolio.get_field_or_template(field_name)


@register.filter
def get_attr(obj, attr_name):
    """
    Dynamically access object attributes inside templates.
    Example:
        {{ portfolio|get_attr:"project1_title" }}
    """
    try:
        return getattr(obj, attr_name)
    except:
        return ""
