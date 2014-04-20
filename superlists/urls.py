from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'superlists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lists.views.home_page'),
    url(r'^lists/(\d+)/$', 'lists.views.view_list'),
    url(r'^lists/new$', 'lists.views.new_list'),
    url(r'^lists/(\d+)/add_item$', 'lists.views.add_item'),

    url(r'^admin/', include(admin.site.urls)),
)
