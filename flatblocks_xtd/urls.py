from django.conf.urls.defaults import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from flatblocks_xtd.views import edit

urlpatterns = patterns('',
    url('^edit/(?P<pk>\d+)/$', staff_member_required(edit),
            name='flatblocks-xtd-edit')
)
