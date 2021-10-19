#!/usr/bin/env python                                                           
# -*- coding: utf-8 -*-                                                         
#                                                                               
# author: Lou Viannay <lou.viannay@octavesolution.com>                                    
from __future__ import print_function, unicode_literals

import re
import logging

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)
register = template.Library()


class Highlighter(object):
    def __init__(self, term, before_term='', new_term=r'\1', after_term=''):
        self.new_text = "{}{}{}".format(before_term, new_term, after_term)
        self.regex = re.compile("({})".format(term), re.IGNORECASE)

    def highlight(self, string):
        return self.regex.sub(self.new_text, string)


def passthru(x):
    return x


@register.filter("hilite", needs_autoescape=True)
@stringfilter
def hilite_search(text, args, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = passthru

    params = [x.strip() for x in args.split(',')]
    search_terms = params.pop(0)

    if not search_terms:
        return mark_safe(esc(text))

    if params:
        klass = params.pop(0)
    else:
        klass = ''
    if params:
        tag = params.pop(0)
    else:
        tag = 'mark'
    if klass:
        before_term = "<{} class=\"{}\">".format(tag, klass)
    else:
        before_term = "<{}>".format(tag)
    after_term = "</{}>".format(tag)
    new_term = r"{}\1{}".format(before_term, after_term)
    terms = [x.strip() for x in search_terms.split()]
    re_terms = r"({})".format("|".join(terms))
    regex_pattern = re.compile(re_terms, re.IGNORECASE)
    result = mark_safe(regex_pattern.sub(new_term, text))
    return mark_safe(esc(result))


def test():
    s = "Insomnia Cookies"
    hiliter = Highlighter('CO', before_term='<span class="hilite">', after_term='</span>')
    print(hiliter.highlight(s))

    return 0
