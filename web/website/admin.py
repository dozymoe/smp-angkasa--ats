"""Tell django contrib admin to only let superusers in
"""
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

class WebsiteAdminSite(admin.AdminSite):
    """Override Admin Site behavior
    """
    def has_permission(self, request):
        """Limit access to superusers
        """
        return request.user.is_active and request.user.is_superuser


class WebsiteAdminConfig(AdminConfig):
    """Override django contrib admin
    """
    default_site = 'website.admin.WebsiteAdminSite'
