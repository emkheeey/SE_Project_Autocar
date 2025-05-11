from django import template
import json

register = template.Library()

@register.filter
def enumerate(iterable):
    """Returns a list of tuples containing (index, item)"""
    return enumerate(iterable)

@register.filter
def json_script(value, element_id):
    """Convert value to JSON string for use in JavaScript"""
    return json.dumps(value)

@register.filter
def get_strengths(comparison_results, car_index):
    """Get list of specifications where this car is a winner"""
    strengths = []
    for spec, data in comparison_results.items():
        if car_index in data['winners'] and data['better'] != 'none':
            strengths.append(data['label'])
    return strengths
