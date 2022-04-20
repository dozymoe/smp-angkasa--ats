import logging
#-
from django.conf import settings
from django.utils import translation
from translated_fields import to_attribute

_logger = logging.getLogger(__name__)


class MultilingualMixin:
    REQUIRED_TRANSLATED_FIELDS = ()
    _is_valid_for_language = None

    def valid_language(self, current=None):
        if current is None:
            current = translation.get_language()
        if current == settings.LANGUAGE_CODE:
            return current

        if self._is_valid_for_language is None:
            self._is_valid_for_language = set()

            for langcode, _ in settings.LANGUAGES[1:]:
                for name in self.REQUIRED_TRANSLATED_FIELDS:
                    if not getattr(self, to_attribute(name, langcode)):
                        break
                else:
                    self._is_valid_for_language.add(langcode)

        if current in self._is_valid_for_language:
            return current
        return settings.LANGUAGE_CODE


    def save(self, update_fields=None, **kwargs):
        if self._is_valid_for_language:
            dirty = set(self.get_dirty_fields().keys())
            if update_fields is not None:
                dirty = set(x for x in dirty if x in update_fields)

            for langcode, _ in settings.LANGUAGES[1:]:
                if self._is_valid_for_language is None:
                    break
                for name in self.REQUIRED_TRANSLATED_FIELDS:
                    trans_name = to_attribute(name, langcode)
                    if trans_name in dirty:
                        self._is_valid_for_language = None
                        break

        return super().save(update_fields=update_fields, **kwargs)


def attrgetter(name, field):
    def getter(self):
        return getattr(self, to_attribute(name, self.valid_language()))
    return getter
