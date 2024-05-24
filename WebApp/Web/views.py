from django.shortcuts import render
from .models import KnowledgeBaseViewerModel, QueryEndpoint
import requests
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .shared import get_filter_uirs_label
from .shared import (extract_data_either_s_p_o_match, format_data_for_kb_single,
                     get_category_value, extract_data_doner_tissuesample_match_query,
                     format_ansrs_data_for_kb_single,
                     format_gars_data_for_kb_single,
                     donor_tissues_data_for_kb_single,
                     get_donor_data_by_id,
                     doner_tissue_to_js,
                     get_tissuesample_data_by_id
                     )


def index(request):
    return render(request, "pages/index.html")


def fetch_knowledge_base(query_or_search_input, query_endpoint_type="get", endpoint_service_type="query"):
    endpoints = QueryEndpoint.objects.all().filter(query_endpoint_type=query_endpoint_type,
                                                   endpoint_service_type=endpoint_service_type)
    payload = {"sparql_query": query_or_search_input}
    response = requests.get(endpoints[0].query_url, params=payload)
    if response.status_code == 200:
        return response.json()


def get_knowledge_base(kbobj):
    labels = get_filter_uirs_label(kbobj)
    query_or_search_input = kbobj[0].sparql_query
    response_data = fetch_knowledge_base(query_or_search_input)
    fetched_data = response_data["message"]["results"]["bindings"]

    if fetched_data:
        return {
            "knowledge_base": kbobj,
            "fetched_data": fetched_data,
            "processed_label": labels["processed_label"],
            "pre_processed_label": labels["pre_processed_label"][0]
        }
    else:
        return {
            "knowledge_base": False
        }


def knowledge_base(request):
    kbobj = KnowledgeBaseViewerModel.objects.all().filter(status_active=True, default_kb=True)
    other_items = KnowledgeBaseViewerModel.objects.all().filter(status_active=True).order_by("-default_kb")
    context = get_knowledge_base(kbobj=kbobj)
    context["menu_items"] = other_items

    return render(request,
                  "pages/knowledge-base.html", context=context)


def knowledge_base_single(request, id):
    param = request.GET.get('uri')
    query = extract_data_either_s_p_o_match(param)

    response_data = fetch_knowledge_base(query)
    fetched_data = response_data["message"]["results"]["bindings"]
    label = id
    formtted_data_all = format_data_for_kb_single(fetched_data)
    formtted_data = formtted_data_all["grouped_data"]
    local_name = formtted_data_all["localname"]

    str_cat = get_category_value(formtted_data)

    tissue_sample_doner = fetch_knowledge_base(extract_data_doner_tissuesample_match_query(str_cat, param))
    tissue_donor_data = tissue_sample_doner["message"]["results"]["bindings"]

    species_value_match_in_gars = [item.strip() for item in
                                   tissue_donor_data[0]["species_value_match_in_gars"]["value"].split(',')]
    matched_nimp_gars_data = format_gars_data_for_kb_single(species_value_match_in_gars, fetch_knowledge_base)

    matched_donor_tissue_details_dict = donor_tissues_data_for_kb_single(tissue_donor_data)

    structure_value_match_in_ansrs = [item.strip() for item in
                                      tissue_donor_data[0]["structure_value_match_in_ansrs"]["value"].split(',')]
    matched_nimp_ansrs_data = format_ansrs_data_for_kb_single(structure_value_match_in_ansrs, fetch_knowledge_base)

    context = {
        "uri_param": param,
        "label": label,
        "local_name": local_name,
        "fetched_data": formtted_data,
        "category": get_category_value(formtted_data),
        "donor_info": matched_donor_tissue_details_dict["donor"],
        "tissuesample_info": matched_donor_tissue_details_dict["tissuesample"],
        "matched_nimp_gars_data": matched_nimp_gars_data,
        "matched_nimp_ansrs_data": matched_nimp_ansrs_data

    }
    return render(request, "pages/knowledge-base-single.html", context=context)


def get_doner_data_ajax(request):
    donor_id = request.GET.get("doner_id")
    try:
        retrieved_doner_data = fetch_knowledge_base(get_donor_data_by_id(donor_id))["message"]["results"]["bindings"]
    except TypeError as e:
        print(e)

    data = {
        'data': doner_tissue_to_js(retrieved_doner_data)
    }
    return JsonResponse(data)


def get_tissuesample_data_ajax(request):
    tissue_id = request.GET.get("tissue_id")
    try:
        retrieved_tissue_data = fetch_knowledge_base(get_tissuesample_data_by_id(tissue_id))["message"]["results"][
            "bindings"]
    except TypeError as e:
        print(e)

    data = {
        'data': doner_tissue_to_js(retrieved_tissue_data)
    }
    return JsonResponse(data)


def knowledge_base_slug(request, slug):
    kbobj = KnowledgeBaseViewerModel.objects.all().filter(slug=slug)
    other_items = KnowledgeBaseViewerModel.objects.all().filter(status_active=True).order_by("-default_kb")
    context = get_knowledge_base(kbobj=kbobj)
    context["menu_items"] = other_items
    return render(request,
                  "pages/knowledge-base.html", context=context)
