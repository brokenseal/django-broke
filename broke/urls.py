from django.conf.urls.defaults import patterns, url


urlpatterns= patterns('broke.views',
    url(r'^$', 'root', {}, 'broke-root'),

    # data urls
    url(r'^data/(?P<app_label>[a-zA-Z0-9_\-]+)/$', 'data', {}, 'broke-data-app'),
    url(r'^data/(?P<app_label>[a-zA-Z0-9_\-]+)/(?P<model_name>[a-zA-Z0-9_\-]+)/$', 'data', {}, 'broke-data-model'),
    url(r'^data/(?P<app_label>[a-zA-Z0-9_\-]+)/(?P<model_name>[a-zA-Z0-9_\-]+)/(?P<pk>[0-9])/$', 'data', {}, 'broke-data-object'),

    # meta data urls
    url(r'^meta_data/$', 'meta_data', {}, 'broke-meta-data'),
    url(r'^meta_data/(?P<app_label>[a-zA-Z0-9_\-]+)/$', 'meta_data', {}, 'broke-meta-app'),
    url(r'^meta_data/(?P<app_label>[a-zA-Z0-9_\-]+)/(?P<model_name>[a-zA-Z0-9_\-]+)/$', 'meta_data', {}, 'broke-meta-model'),
)