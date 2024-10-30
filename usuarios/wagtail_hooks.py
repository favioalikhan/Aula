"""
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from wagtail import hooks

def get_viewset_cls(app_config, viewset_name):
    try:
        viewset_cls = import_string(getattr(app_config, viewset_name))
    except (AttributeError, ImportError) as e:
        raise ImproperlyConfigured(
            f"Invalid setting for {app_config.__class__.__name__}.{viewset_name}: {e}"
        )
    return viewset_cls


@hooks.register("register_admin_viewset")
def register_viewset():
    app_config = apps.get_app_config("wagtailusers")
    user_viewset_cls = get_viewset_cls(app_config, "user_viewset")
    group_viewset_cls = get_viewset_cls(app_config, "group_viewset")
    return [
        user_viewset_cls("wagtailusers_users", url_prefix="users"),
        group_viewset_cls("wagtailusers_groups", url_prefix="groups"),
    ]
"""

from wagtail.admin.views.account import NameEmailSettingsPanel
from .wagtail_forms import CustomNameEmailForm
from functools import cached_property
from django.utils.translation import gettext as _
from django.conf import settings


def email_management_enabled():
    return getattr(settings, "WAGTAIL_EMAIL_MANAGEMENT_ENABLED", True)


class CustomNameEmailSettingsPanel(NameEmailSettingsPanel):

    name = "name_email"
    order = 100
    form_class = CustomNameEmailForm

    @cached_property
    def title(self):
        if email_management_enabled():
            return _("Name and Email")
        return _("Name")
