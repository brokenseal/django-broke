
registered_models = {}

def register(model):
    app_label= model._meta.app_label

    if not registered_models.has_key(app_label):
        registered_models.setdefault(app_label, [])

    registered_models[app_label].push(model)
