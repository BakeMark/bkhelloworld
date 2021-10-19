#!/usr/bin/env python                                                           
# -*- coding: utf-8 -*-                                                         
#                                                                               
# author: Lou Viannay <lou@islandtechph.com>

from django import template

# from external_db.models import get_branch_choices

register = template.Library()


@register.filter
def dlookup(d, key):
    return d.get(key, '')


@register.filter
def index(indexable, i):
    if hasattr(indexable, str(i)):
        return getattr(indexable, str(i), '')
    else:
        return indexable[i]


@register.simple_tag(takes_context=True)
def pathstartswith(context, path_arg, *args, **kwargs):
    request = context['request']
    actual_path = request.path
    try:
        active = args[0]
    except IndexError:
        active = "active"

    try:
        not_active = args[1]
    except IndexError:
        not_active = ""

    index_arg = kwargs.get('index') or 1

    path_part = path_arg.split('/')
    paths = actual_path.split('/')

    for i, p in enumerate(path_part):
        if paths[index_arg + i] != p:
            return not_active
    return active
    # extra = "({}) '{}'".format(index, paths[index])
    # if paths[index] == path_part:
    #    return active  # + extra
    # else:
    #   return not_active  # + extra + str(paths)


# @register.inclusion_tag('branch_select.html')
# def branch_selection():
#     choices = get_branch_choices()
#     return {'choices': choices}


@register.inclusion_tag('pagination.html')
def mkpageli(page_obj, display_count=10, url_str='?page={}', **kwargs):
    num_pages = page_obj.paginator.num_pages
    current_page = page_obj.number

    _max = current_page + (display_count // 2)
    if _max > num_pages:
        _max = num_pages

    _min = _max - display_count
    if _min < 1:
        _min = 1
        _max = min(num_pages, display_count + 1)

    if num_pages - _max == 1:
        _max = num_pages

    if _min == 2:
        _min = 1

    pages = []
    for pg in range(_min, _max + 1):
        url = url_str.format(pg, **kwargs)
        if pg == current_page:
            class_str = "active"
        else:
            class_str = ""
        pages.append({
            "page": pg,
            "url": url,
            "class": class_str,
        })

    result = {'pages': pages, 'show_first': _min != 1, 'show_last': _max != num_pages, 'has_pages': num_pages > 1,
              'last_page': num_pages, 'next_page': min(current_page + 1, num_pages),
              'prev_page': max(current_page - 1, 1)}

    return result

    #        "min_page = {}, max_page = {} current_page = {}".format(
    #    _min,
    #    _max,
    #    current_page,
    # )
