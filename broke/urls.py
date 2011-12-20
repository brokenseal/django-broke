from django.conf.urls.defaults import patterns, url


urlpatterns= patterns('broke.views',
    url(r'^/$', 'root', {}, 'broke-root'),

    # data urls
    url(r'^data/(?P<app_label>\w)/$', 'data', {}, 'broke-data-app'),
    url(r'^data/(?P<app_label>\w)/(?P<model_name>\w)/$', 'data', {}, 'broke-data-model'),
    url(r'^data/(?P<app_label>\w)/(?P<model_name>\w)/(?P<pk>\w)/$', 'data', {}, 'broke-data-object'),

    # meta data urls
    url(r'^meta_data/$', 'meta_data', {}, 'broke-meta-data'),
    url(r'^meta_data/(?P<app_label>\w)/$', 'meta_data', {}, 'broke-meta-app'),
    url(r'^meta_data/(?P<app_label>\w)/(?P<model_name>\w)/$', 'meta_data', {}, 'broke-meta-model'),
)