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
# @File    : shared.py
# @Software: PyCharm

from urllib.parse import urlparse
import json

import textwrap
from collections import defaultdict

def extract_uri_data(url):
    parsed_url = urlparse(url)
    if parsed_url.fragment:
        return parsed_url.fragment
    else:
        return parsed_url.path.split('/')[-1]


def filter_data(list_of_dict, filter_uris):
    filtered_data = [entry for entry in list_of_dict if entry['p']['value'] in filter_uris]
    return filtered_data


def capitalize_first_letter_only(text):
    if text:
        return text[0].upper() + text[1:]
    return text


def format_sentence(text):
    formatted_text = text.replace('_', ' ').capitalize()
    return formatted_text


def get_filter_uirs_label(kbobj):
    label_list = []
    original_label = []
    column_names = ['display_column_first', 'display_column_second', 'display_column_third', 'display_column_fourth']
    for column in column_names:
        column_data = getattr(kbobj[0], column, None)

        if column_data:
            try:
                original_label.append(column_data)
                if '_' in column_data:
                    label_list.append(format_sentence(column_data))
                else:
                    label_list.append(capitalize_first_letter_only(column_data))
            except Exception as e:
                print(f"An error occurred while processing {column}: {e}")

    return {"processed_label": label_list,
            "pre_processed_label":
                original_label
            }


def extract_data_either_s_p_o_match(param):
    query = textwrap.dedent(
        """SELECT ?subject ?predicate ?object
  WHERE {{
    {{ BIND(<{0}> AS ?id)
      ?subject ?predicate ?id . }}
    UNION
    {{ BIND(<{0}> AS ?id)
      ?id ?predicate ?object . }}
    UNION
    {{ BIND(<{0}> AS ?id)
      ?subject ?id ?object . }}
  }}"""
    ).format(param)
    return query

def group_dict(list_of_dict):
    grouped_data = defaultdict(list)
    for item in list_of_dict:
        grouped_data[item['property']].append(item['value'])

    # Creating a list of dictionaries with the grouped data, ensuring lists are only used when needed
    result = []
    for key, values in grouped_data.items():
        if len(values) > 1:
            result.append({'property': key, 'value': values})
        else:
            result.append({'property': key, 'value': values[0]})  # Only take the single value out of the list

    return result


def format_data_for_kb_single(fetched_data):
    data_to_display = []


    for data in fetched_data:
        if 'object' in data and data['object'] is not None:
            data_to_display.append({"property": data['predicate']['value'],
                                    "value":data['object']['value']}
                                   )
    grouped_data  = group_dict(data_to_display)
    print(grouped_data)
    return grouped_data