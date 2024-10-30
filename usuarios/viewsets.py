from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.panels import FieldPanel
from .models import CustomUser
from wagtail.users.models import UserProfile
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, override
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.auth import update_session_auth_hash
from collections import OrderedDict
from wagtail.log_actions import log
from wagtail import hooks
from django.forms.widgets import Media
from wagtail.admin.views.account import (
    AccountView,
    AvatarSettingsPanel,
    NotificationsSettingsPanel,
    LocaleSettingsPanel,
    ThemeSettingsPanel,
    ChangePasswordPanel,
)


# Reemplaza la secciónd de usuarios del panel de wagtail (wagtailusers)
class CustomUserViewSet(ModelViewSet):
    model = CustomUser
    panels = [
        FieldPanel("username"),
    ]
    icon = "user"
    inspect_view_enabled = True


custom_user_viewset = CustomUserViewSet("custom_user")


@method_decorator(sensitive_post_parameters(), name="post")
class CustomAccountView(AccountView):

    template_name = (
        "usuarios/custom_account_wagtail.html"  # Puedes usar tu propio template
    )
    page_title = gettext_lazy("Cuenta personal")  # Personaliza el título
    header_icon = "user"

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario no está autenticado, redirige al login de Wagtail
        if not request.user.is_authenticated:
            return redirect("wagtailadmin_login")  # Redirige al login de Wagtail

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panels = self.get_panels()
        context["panels_by_tab"] = self.get_panels_by_tab(panels)
        context["menu_items"] = self.get_menu_items()
        context["media"] = self.get_media(panels)
        context["user"] = self.request.user
        return context

    def get_panels(self):
        request = self.request
        user = self.request.user
        profile = UserProfile.get_for_user(user)
        from .wagtail_hooks import CustomNameEmailSettingsPanel

        # Aquí puedes personalizar qué paneles quieres mostrar
        panels = [
            CustomNameEmailSettingsPanel(
                request, user, profile
            ),  # Tu panel personalizado
            AvatarSettingsPanel(request, user, profile),
            NotificationsSettingsPanel(request, user, profile),
            LocaleSettingsPanel(request, user, profile),
            ThemeSettingsPanel(request, user, profile),
            ChangePasswordPanel(request, user, profile),
        ]

        # Mantén esto si quieres permitir que otros hooks agreguen paneles
        for fn in hooks.get_hooks("register_account_settings_panel"):
            panel = fn(request, user, profile)
            if panel and panel.is_active():
                panels.append(panel)

        panels = [panel for panel in panels if panel.is_active()]
        return panels

    def get_panels_by_tab(self, panels):
        tabs = list({panel.tab for panel in panels})
        tabs.sort(key=lambda tab: tab.order)

        panels_by_tab = OrderedDict([(tab, []) for tab in tabs])
        for panel in panels:
            panels_by_tab[panel.tab].append(panel)
        for tab, tab_panels in panels_by_tab.items():
            tab_panels.sort(key=lambda panel: panel.order)
        return panels_by_tab

    def get_menu_items(self):
        menu_items = []
        for fn in hooks.get_hooks("register_account_menu_item"):
            item = fn(self.request)
            if item:
                menu_items.append(item)
        return menu_items

    def get_media(self, panels):
        panel_forms = [panel.get_form() for panel in panels]
        media = Media()
        for form in panel_forms:
            media += form.media
        return media

    def post(self, request):
        panel_forms = [panel.get_form() for panel in self.get_panels()]
        user = self.request.user
        profile = UserProfile.get_for_user(user)

        if all(form.is_valid() or not form.is_bound for form in panel_forms):
            with transaction.atomic():
                for form in panel_forms:
                    if form.is_bound:
                        form.save()

            log(user, "wagtail.edit")

            update_session_auth_hash(request, user)

            with override(profile.get_preferred_language()):
                messages.success(
                    request, _("¡Tus datos han sido actualizados exitosamente!")
                )

            return redirect(
                "wagtailadmin_account"
            )  # Nota: usamos el nuevo nombre de URL

        return TemplateResponse(request, self.template_name, self.get_context_data())
