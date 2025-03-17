from django import template
register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get attribute from an object dynamically"""
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        try:
            return obj[attr]
        except (KeyError, TypeError):
            return None

@register.filter
def divided_by(value, arg):
    """Divides the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return ''
    
