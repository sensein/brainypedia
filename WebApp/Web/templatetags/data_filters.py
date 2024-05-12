# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : data_filters.py
# @Software: PyCharm
from django import template
from urllib.parse import urlparse
import validators
register = template.Library()

def format_underscore_string(s):
    if "_" in s:
        words = s.split('_')
        words = [word.capitalize() for word in words]
        formatted_string = ' '.join(words)
        return formatted_string
    else:
        return s
@register.filter
def extract_last_part(value):
    if '#' in value:
        last_part = value.split('#')[-1]
    else:
        last_part = value.split('/')[-1]
    last_part = format_text_with_space(format_underscore_string(last_part))
    return last_part

@register.filter
def extract_last_two_part(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    parts = path.lstrip('/').split('/')
    formatted_data = ':'.join(parts[-2:])
    return formatted_data

@register.filter
def capitalize_first_letter(value):
    if value:
        return value[0].upper() + value[1:]
    else:
        return ""

@register.filter
def format_text_with_space(text):
    # convert wasDerivedFrom to Was Derived From
    words = []
    start = 0

    for i in range(1, len(text)):
        if text[i].isupper():
            words.append(text[start:i])
            start = i

    words.append(text[start:])
    words[0] = words[0].capitalize()
    formatted_text = " ".join(words)

    return formatted_text

@register.filter
def is_list(item):
    return type(item) == list

@register.filter
def is_url(string):
    return validators.url(string)