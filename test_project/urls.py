from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url('^flatblocks-xtd/', include("flatblocks_xtd.urls")),
    url('^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        "",
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
        }),
    )
    
urlpatterns += patterns('',
    url('^/?', views.index),
)
