"""fireh_runner configuration adapter
"""
from .configuration import flatten_dict

def django_conf_adapter(prefix, new, setter):
    """Custom configuration adapter for Django
    """
    exceptions = [
        'database.options',
        'logging.handlers',
    ]
    setter.update(flatten_dict(prefix, new, exceptions))
