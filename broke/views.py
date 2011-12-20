import json

from django import http
from django.core import serializers
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from broke.registration import registered_models
from broke import settings, managers


encoder= serializers.get_serializer(settings.ENCODER)()
Http400= http.HttpResponseBadRequest(ugettext("There are no registered models on this app."))


def root(request):
    for app_label, models in registered_models:
        pass

    return Http400

def data(request, app_label, model_name=None, pk=None, filter_kwargs=None, exclude_kwargs=None):
    """
        Retrieve data based on the app or the model or just for a single model instance
        It's possible to filter results using the DEFAULT_MANAGER and MODEL_MANAGERS settings
    """
    models= registered_models.get(app_label, None)
    
    if models is None:
        return Http400
    
    if model_name is not None:
        # retrieve the correct model
        models= [ model for model in models if model.__name__ == model_name ]
        
    data= {}
    default_manager_name= settings.DEFAULT_MANAGER
    
    for model in models:
        model_name= model.__name__
        model_id= "%s.%s" % (app_label, model_name,)
        
        # get manager name
        manager_name= settings.MODEL_MANAGERS.get(model_id, default_manager_name)
        manager= getattr(model, manager_name)

        # if the manager is an instance of BrokeManager, allow filtering based on some computation
        # around the request object
        if isinstance(manager, managers.BrokeManager):
            manager = manager.filter_based_on_request(request)

        # retrieve data
        if filter_kwargs is not None:
            manager = manager.filter(**filter_kwargs)
        if exclude_kwargs is not None:
            manager = manager.exclude(**exclude_kwargs)

        if pk is None:
            data_set= manager.all()
        else:
            try:
                data_set= (manager.get(pk),)
            except model.DoesNotExist:
                raise http.Http404
                    
        data.setdefault(model_name, encoder.serialize(data_set))

    return json.dumps(data)
    
def _get_meta_data(app_label, model_name=None):
    """
        Retrieve models meta data
    """
    models= registered_models.get(app_label, None)

    if models is None:
        return Http400

    if model_name is not None:
        models= [ model for model in models if model.__name__ == model_name ]

    meta_data= {}

    for model in models:
        _meta_data={}

        for field in model._meta.fields:
            _meta_data.setdefault(field.name, field.__class__.__name__)

        meta_data.setdefault(model.__name__, _meta_data)

    return meta_data

def meta_data(request, app_label, model_name=None):
    return encoder(_get_meta_data(app_label, model_name))

def render_models_meta_data(app_label, model_name=None, apps_namespace=''):
    app_models= _get_meta_data(app_label, model_name)
    return render_to_string('broke/models_meta_data.html', locals())