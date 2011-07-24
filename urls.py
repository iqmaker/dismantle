# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'dismantle.core.views.index'),
    (r'^razborka/', include('dismantle.core.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'} ), #redirect_field_name,authentication_form
    (r'^logout/$', 'dismantle.core.views.mylogout' ),
    (r'^registration/$', 'dismantle.core.views.registration' ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT }),)
