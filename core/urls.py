# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    (r'^$', 'index'),
    (r'^blogs$', 'blogs'),
    (r'^about$', 'about'),
    (r'^feedback$', 'feedback'),
    (r'^region$', 'region'),
    (r'^mansearch$', 'mansearch'),
    (r'^modelsearch$', 'modelsearch'),
    (r'^changepassword$', 'changepassword'),
    (r'^todolist$', 'todolist' ),
    
    (r'^ajax/manufacture_models/$', 'manufacture_models'),
    (r'^ajax/region_by_state/$', 'region_by_state'),
    (r'^ajax/city_by_region/$', 'city_by_region'),
    
    (r'^(?P<manufacture_title>[\w\-]+)/(?P<model_title>[\w\-]+)/region-(?P<region_title>[\w\-]+)/gorod-(?P<city_title>[\w\-]+)$', 'alias_index'),
    (r'^(?P<manufacture_title>[\w\-]+)/(?P<model_title>[\w\-]+)/region-(?P<region_title>[\w\-]+)$', 'alias_index'),
    (r'^(?P<manufacture_title>[\w\-]+)/(?P<model_title>[\w\-]+)', 'alias_index'),
    (r'^(?P<manufacture_title>[\w\-]+)', 'alias_index'),
    
    (r'^(?P<manufacture_title>[\w\-]+)/region\-(?P<region_title>[\w\-]+)', 'alias_index'),
)