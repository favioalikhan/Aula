from unfold.sites import UnfoldAdminSite
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm


class AulaAdminSite(UnfoldAdminSite):
    # General configuration
    site_title = _("Aula Admin")
    site_header = _("Aula Admin")
    index_title = _("Dashboard")
    login_form = LoginForm

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request, app_label)
        return sorted(app_list, key=lambda x: x["name"].lower())


aula_admin_site = AulaAdminSite(name="aula_admin")
