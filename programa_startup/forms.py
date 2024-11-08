from django import forms
from .models import Startup, IntegranteStartup, Entregable, Sesion, Tarea, Logro
from usuarios.widgets import CustomStartupImageWidget
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.core.exceptions import ValidationError


class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = (
            "nombre",
            "descripcion",
            "logo",
            "problematica",
            "propuesta_valor",
            "publico_objetivo",
            "socios_clave",
            "canales",
            "producto_servicio",
        )
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Ingrese el nombre de su Startup",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Descripción de tu Startup",
                }
            ),
            "logo": CustomStartupImageWidget(
                attrs={"class": "hidden", "accept": "image/*"}
            ),
            "problematica": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Problemática",
                }
            ),
            "propuesta_valor": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Propuesta de valor de su Startup",
                }
            ),
            "publico_objetivo": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Defina su público objetivo",
                }
            ),
            "socios_clave": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Mencione los socios clave",
                }
            ),
            "canales": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Defina los canales de distribución",
                }
            ),
            "producto_servicio": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Describa su producto o servicio",
                }
            ),
        }

    def clean_startup_image(self):
        image = self.cleaned_data.get("logo", False)
        if image:
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("La imagen de startup excede los 10MB.")
            if image.content_type not in [
                "image/png",
                "image/jpeg",
                "image/svg+xml",
                "image/x-xbitmap",
                "image/tiff",
                "image/vnd.microsoft.icon",
                "image/x-icon",
                "image/gif",
                "image/webp",
                "image/apng",
                "image/pjpeg",
                "image/avif",
                "image/bmp",
                "image/jfif",
                "image/pjp",
            ]:
                raise forms.ValidationError(
                    "Tipo de archivo no soportado para la imagen de startup."
                )
        return image

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo == FILE_INPUT_CONTRADICTION:
            raise ValidationError(
                "No puedes subir una nueva imagen y eliminar la existente al mismo tiempo."
            )
        elif logo is False:
            # Usuario ha marcado el checkbox de eliminación
            return False
        elif not logo:
            # No se subió un nuevo archivo y no se marcó el checkbox
            return self.instance.logo
        else:
            # Se subió un nuevo archivo
            return logo

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("logo") is False:
            # Establecer foto_perfil en None para eliminarla
            user.logo = None
        if commit:
            user.save()
        return user


class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = ["titulo", "descripcion", "fecha_logro"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "id": "titulo",
                    "name": "nuevo_logro_titulo",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Ingrese el título del logro",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "id": "descripcion",
                    "name": "nuevo_logro_descripcion",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "rows": 3,
                    "placeholder": "Describa el logro obtenido",
                }
            ),
            "fecha_logro": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "fecha_logro",
                    "name": "nuevo_logro_fecha",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                },
                format="%Y-%m-%d",
            ),
        }


class IntegranteStartupForm(forms.ModelForm):
    class Meta:
        model = IntegranteStartup
        fields = ["usuario", "cargo"]
        widgets = {
            "usuario": forms.TextInput(
                attrs={
                    "class": "search-user-input w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Usuario",
                    "value": "{{integrante.usuario.username}}",
                }
            ),
            "cargo": forms.TextInput(
                attrs={
                    "class": "cargo-input w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Cargo",
                    "value": "{{integrante.cargo}}",
                }
            ),
        }


class EditIntegranteForm(forms.ModelForm):
    class Meta:
        model = IntegranteStartup
        fields = ["cargo"]
        widgets = {
            "cargo": forms.TextInput(attrs={"class": "form-control"}),
        }


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Entregable
        fields = [
            "calificacion",
            "comentario",
            "estado",
        ]  # Incluye los campos que quieres permitir editar
        widgets = {
            "calificacion": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                    "min": 0,
                    "max": 20,
                    "step": 0.1,
                }
            ),
            "comentario": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                    "rows": 4,
                }
            ),
            "estado": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                    "disabled": "disabled",  # Deshabilitar el campo
                }
            ),
        }


class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = [
            "titulo",
            "tipo",
            "archivo",
            "url_externa",
        ]  # Campos que deseas permitir editar


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = [
            "titulo",
            "descripcion",
            "fecha_entrega",
            "archivo",
            "tipo",
            "bloqueado",
        ]  # Campos que deseas permitir editar


class EntregableForm(forms.ModelForm):

    archivo = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",  # O las clases CSS que prefieras
                "accept": "*/*",  # Aceptar cualquier tipo de archivo
            }
        ),
    )

    class Meta:
        model = Entregable
        fields = [
            "archivo",
            "estado",
        ]  # Campos del modelo que quieres que se incluyan en el formulario

        widgets = {
            "estado": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                    "readonly": "readonly",  # Hace que el campo sea solo lectura
                }
            ),
        }
