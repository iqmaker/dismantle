# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    (r'^$', 'index'),
    (r'^(?P<regionid>\d{1,4})-(?P<manufactureid>\d{1,4})-(?P<modelid>\d{1,4})\-(?P<pageid>\d{1,4})\.html', 'index'),
    (r'^(?P<region_title>\w+)\-(?P<manufacture_title>\w+)\-(?P<model_title>\w+)\-(?P<page_num>\w+)\.html', 'alias_index'),
    (r'^blogs$', 'blogs'),
    (r'^dismantle-add$', 'dismantle_add'),
    (r'^about$', 'about'),
    (r'^feedback$', 'feedback'),
    (r'^region$', 'region'),
    (r'^mansearch/$', 'mansearch'),
    (r'^modelsearch/$', 'modelsearch'),
    (r'^ajax/manufacture_models/$', 'manufacture_models'),
)