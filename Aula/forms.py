from django import forms
from django.conf import settings
from unfold.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # Usar 'getattr' con valores por defecto para evitar el error
        login_username = getattr(settings, "LOGIN_USERNAME", None)
        login_password = getattr(settings, "LOGIN_PASSWORD", None)

        if login_username and login_password:
            self.fields["email"].initial = login_username
            self.fields["password"].initial = login_password
