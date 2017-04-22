"""
DictSupport

Provides functions that aid dictionary look ups within the system.

=== Methods ===

get_item -- Given a dictionary and a key, the function returns the object linked to that key.

                :parameter (dict) dictionary - dictionary to be worked with
                           (obj) key --------- key for dictionary look up
                :return (obj) the object linked to the 'key' parameter in the dictionary
                
"""

from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
