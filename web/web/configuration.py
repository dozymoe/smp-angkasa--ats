from misc.configuration import flatten_dict

def config_adapter(prefix, new, setter):
    exceptions = [
        'logging.handlers',
    ]
    setter.update(flatten_dict(prefix, new, exceptions))
