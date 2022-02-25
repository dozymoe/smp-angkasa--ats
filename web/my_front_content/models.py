from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
#-
from web_page.models import WebPage


class FrontContent(DirtyFieldsMixin, RulesModel):
    content = models.ForeignKey(WebPage, verbose_name=_("Content"),
            on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_front_contents')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


    class Meta:

        get_latest_by = 'created_at'
        ordering = ['-created_at']
        rules_permissions = {
            'add': rules.is_staff,
            'read': rules.always_allow,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.content.title
