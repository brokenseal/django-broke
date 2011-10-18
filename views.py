from django import http
from django.core import serializers
from django.utils.translation import ugettext

from . import settings
from .registration import registered_models


encoder= serializers.get_serializer(settings.ENCODER)
Http400= http.HttpResponseBadRequest(ugettext("There are no registered models on this app."))


def root(request):
    for app_label, models in registered_models:
        pass
        

def data(request, app_label, model_name=None, pk=None):
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

        # retrieve data
        if pk is None:
            data_set= manager.all()
        else:
            try:
                data_set= (manager.get(pk),)
            except model.DoesNotExist:
                raise http.Http404
                    
        data.setdefault(model_name, data_set)

    return encoder(data)
        
def meta_data(request, app_label, model_name=None):
    """
        Retrieve models description
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
        
    return encoder(meta_data)