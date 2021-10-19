#!/usr/bin/env python                                                           
# -*- coding: utf-8 -*-                                                         
#                                                                               
# author: Lou Viannay <lou.viannay@octavesolution.com>                                    
from __future__ import print_function, unicode_literals

from debug_toolbar.middleware import show_toolbar as orig_show_toolbar


def show_toolbar(request):
    show_flag = orig_show_toolbar(request)
    if show_flag:
        paths = request.path_info.split('/')
        show_flag = 'admin' not in paths

    return show_flag


