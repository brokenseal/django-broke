from django.conf import settings

BROKE_DEFAULTS= {
    # if set, it should be a valid instance of django.db.models.Manager
    # use this if you want to filter querysets
    'DEFAULT_MANAGER': '_default_manager',
    
    # just like DEFAULT_MANAGER it allows you to set a manager to retrieve data, based on the single model
    # e.g. MODEL_MANAGERS= {
    #   'myapp.MyModel': 'my_manager',
    # }
    'MODEL_MANAGERS': {},

    # set this to whatever encoder you want to use
    # available values are the same as the ones django supports: xml, json and yaml
    'ENCODER': 'json',
}

# merge default settings with user's settings
BROKE_DEFAULTS.update(settings.BROKE or {})

# update local module scope with broke specific settings
locals().update(BROKE_DEFAULTS)