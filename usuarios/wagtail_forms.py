from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from wagtail.admin.forms.account import NameEmailForm

User = get_user_model()


class CustomNameEmailForm(NameEmailForm):
    """
    Formulario personalizado para la gestión de nombre y correo electrónico
    """

    username = forms.CharField(
        required=False,
        label=_("Nombre"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Ingrese su nombre")}
        ),
    )

    apellido_paterno = forms.CharField(
        required=True,
        label=_("Apellido paterno"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Ingrese sus apellido paterno"),
            }
        ),
    )

    apellido_materno = forms.CharField(
        required=True,
        label=_("Apellido materno"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Ingrese sus apellido materno"),
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        label=_("Correo electrónico"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("ejemplo@correo.com")}
        ),
    )
    first_name = None
    last_name = None

    def __init__(self, *args, **kwargs):
        from wagtail.admin.views.account import email_management_enabled

        super().__init__(*args, **kwargs)

        # Mantiene la lógica de gestión de correo electrónico de Wagtail
        if not email_management_enabled():
            del self.fields["email"]

        # Puedes agregar validaciones adicionales o modificar los campos aquí
        for field in self.fields.values():
            field.error_messages = {
                "required": _("Este campo es obligatorio"),
                "invalid": _("Ingrese un valor válido"),
            }

    def clean_email(self):
        """
        Validación personalizada para el campo de correo electrónico
        """
        email = self.cleaned_data.get("email")
        if email:
            # Verifica si el correo ya existe (excepto para el usuario actual)
            existing_users = User.objects.filter(email=email)
            if self.instance.pk:
                existing_users = existing_users.exclude(pk=self.instance.pk)
            if existing_users.exists():
                raise forms.ValidationError(
                    _("Este correo electrónico ya está registrado")
                )
        return email

    def clean(self):
        """
        Validaciones adicionales que involucran múltiples campos
        """
        cleaned_data = super().clean()
        # Puedes agregar validaciones personalizadas aquí
        return cleaned_data

    class Meta:
        model = User
        fields = ["username", "apellido_paterno", "apellido_materno", "email"]
