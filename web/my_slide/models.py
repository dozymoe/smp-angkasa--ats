from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
from translated_fields import TranslatedField
#-
from my_files.models import MyFile
from website.mixins import MultilingualMixin, attrgetter


AVAILABLE_SLIDES = (
        ('front', _("Front Page")),
        )

class MySlide(DirtyFieldsMixin, MultilingualMixin, RulesModel):
    REQUIRED_TRANSLATED_FIELDS = ('description',)

    location = models.CharField(verbose_name=_("Location"), max_length=12,
            choices=AVAILABLE_SLIDES, db_index=True)
    position = models.PositiveIntegerField(verbose_name=_("Position"),
            db_index=True, default=0)

    description = TranslatedField(
            models.TextField(verbose_name=_("Description"), null=True,
                blank=True),
            attrgetter=attrgetter)

    image = models.ForeignKey(MyFile, verbose_name=_("Image"),
            on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_slides')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


    class Meta:

        get_latest_by = 'created_at'
        ordering = ['-created_at']
        rules_permissions = {
            'add': rules.is_authenticated,
            'read': rules.always_allow,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.location
