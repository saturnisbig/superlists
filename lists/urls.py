from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'superlists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(\d+)/$', 'lists.views.view_list'),
    url(r'^new$', 'lists.views.new_list'),
    url(r'^(\d+)/add_item$', 'lists.views.add_item'),

)
