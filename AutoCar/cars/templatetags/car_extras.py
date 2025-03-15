from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get attribute from an object dynamically"""
    return getattr(obj, attr, None)  # This uses Python's built-in getattr

@register.filter
def divided_by(value, arg):
    """Divides the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return ''
    
