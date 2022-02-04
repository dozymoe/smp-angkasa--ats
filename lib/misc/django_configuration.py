from .configuration import flatten_dict


def django_conf_adapter(prefix, new, setter):
    exceptions = [
        'database.options',
    ]
    setter.update(flatten_dict(prefix, new, exceptions))
