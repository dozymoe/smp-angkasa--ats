"""Django Views decorators
"""
from functools import wraps
import logging
#-
from django.conf import settings
from django.utils.decorators import method_decorator
#_
from website.tasks import freeze_view

_logger = logging.getLogger()

def thawed_view(view_name : str):
    """outer wrapper
    """
    def decorator(view):
        """inner wrapper
        """
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            """Regenerate static cache files

            If this view is accessed, that means the cache was pruned and need to
            be regenerated.
            """
            if request.resolver_match:
                host = request.get_host()
                lang = request.LANGUAGE_CODE
                dest = settings.FROZEN_ROOT.get(host)
                if dest:
                    dest = str(settings.ROOT_DIR / dest)
                freeze_view.delay(view_name, host=host, langcode=lang, dest=dest,
                        **kwargs)

            return view(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def thawed_class_view():
    """outer wrapper
    """
    def decorator(View):
        """inner wrapper
        """
        view_name = f'{View.__module__}.{View.__qualname__}'
        return method_decorator(thawed_view(view_name), name='dispatch')(View)

    return decorator
