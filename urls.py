from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
import settings
from vim.api import Search

admin.autodiscover()

urlpatterns = []

# app_name Patterns
urlpatterns += patterns('vim.views',
    # Place your patterns here
    # url(r'^$', 'signup_view'),
    url(r'^$', direct_to_template, {'template': 'home.html'}),
)

urlpatterns += patterns('vim.api',
    # API endpoint URLs go-here here
    url(r'^api/search/', Search),
)

# Admin and static file patterns
urlpatterns += patterns('',
    # Enable admin:
    url(r'^admin/', include(admin.site.urls)),

    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Allow for a superuser to be created if one does not exist.
    # You're basically asking to be hacked by leaving this uncommented.
    # url(r'^createuser/', 'views.createuser'),

    # Serve static files.
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
