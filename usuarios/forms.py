from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import CustomUser, Emprendedor, Mentor, Mentoria
from .widgets import CustomProfileImageWidget
from django.contrib.auth import get_user_model


class CustomUserSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "apellido_paterno",
            "apellido_materno",
            "dni",
            "celular",
            "genero",
            "ocupacion",
            "fecha_nacimiento",
            "foto_perfil",
            "red_social",
        ]
        labels = {
            "username": "Nombre",
            "apellido_paterno": "Apellido Paterno",
            "apellido_materno": "Apellido Materno",
            "email": "Correo electrónico",
            "dni": "DNI",
            "celular": "Celular",
            "genero": "Género",
            "ocupacion": "Ocupación",
            "fecha_nacimiento": "Fecha de nacimiento",
            "foto_perfil": "Foto de perfil",
            "red_social": "Red social",
        }
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "genero": forms.Select(
                choices=[
                    ("", "Seleccione género"),
                    ("M", "Masculino"),
                    ("F", "Femenino"),
                    ("O", "Otro"),
                ]
            ),
        }


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "@email.com",
            }
        ),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "Nombre de usuario",
            }
        ),
    )

    apellido_paterno = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "Apellido paterno",
            }
        ),
    )
    apellido_materno = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "Apellido materno",
            }
        ),
    )

    genero = forms.ChoiceField(
        choices=[("", "Seleccione género")] + CustomUser.GENDER_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4"
            }
        ),
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-navy-blue mb-4",
            }
        ),
        required=True,
    )

    REGISTER_ROLES = [
        (CustomUser.EMPRENDEDOR, "Emprendedor"),
        (CustomUser.MENTOR, "Mentor"),
    ]
    rol = forms.ChoiceField(
        choices=REGISTER_ROLES,
        required=True,
        widget=forms.RadioSelect(attrs={"class": "form-radio text-blue-600"}),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "***************",
                "id": "password1",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md text-navy-blue mb-4",
                "placeholder": "***************",
                "id": "password2",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "apellido_paterno",
            "apellido_materno",
            "genero",
            "fecha_nacimiento",
            "rol",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.clean_username()
        user.email = self.cleaned_data["email"]
        user.apellido_paterno = self.cleaned_data["apellido_paterno"]
        user.apellido_materno = self.cleaned_data["apellido_materno"]
        user.genero = self.cleaned_data["genero"]
        user.fecha_nacimiento = self.cleaned_data["fecha_nacimiento"]
        user.rol = self.cleaned_data["rol"]

        if user.rol == CustomUser.ADMINISTRADOR:
            user.is_staff = True
            user.is_superuser = True
        elif user.rol == CustomUser.SPEAKER:
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


class UserCustomChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "apellido_paterno",
            "apellido_materno",
            "dni",
            "celular",
            "genero",
            "rol",
            "foto_perfil",
            "fecha_nacimiento",
            "ocupacion",
            "red_social",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.rol == CustomUser.ADMINISTRADOR:
            user.is_staff = True
            user.is_superuser = True
        elif user.rol == CustomUser.SPEAKER:
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            "foto_perfil",
            "dni",
            "username",
            "apellido_paterno",
            "apellido_materno",
            "email",
            "celular",
            "genero",
            "fecha_nacimiento",
            "ocupacion",
            "red_social",
        )

        widgets = {
            "foto_perfil": CustomProfileImageWidget(
                attrs={"class": "hidden", "accept": "image/*"}
            ),
            "dni": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "DNI",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Nombres",
                }
            ),
            "apellido_paterno": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Apellido paterno",
                }
            ),
            "apellido_materno": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Apellido materno",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "@Email.com",
                }
            ),
            "celular": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "+51",
                }
            ),
            "genero": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "disabled": "disabled",
                    "placeholder": "Género",
                }
            ),
            "fecha_nacimiento": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "type": "date",
                    "disabled": "disabled",
                }
            ),
            "ocupacion": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Ocupación",
                }
            ),
            "red_social": forms.URLInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "URL de su red social",
                }
            ),
        }


class EmprendedorForm(forms.ModelForm):
    class Meta:
        model = Emprendedor
        fields = (
            "resumen_perfil",
            "universidad",
            "facultad",
            "escuela",
            "grado_instruccion",
            "sectores_interes",
            "habilidades_blandas",
        )
        widgets = {
            "resumen_perfil": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Escribe aquí tu biografía...",
                }
            ),
            #'cargo': forms.TextInput(attrs={
            #     'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500',
            #     'placeholder': 'No te asignaron un cargo'
            # }),
            # 'startup': forms.TextInput(attrs={
            #      'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500',
            #      'placeholder': 'No estás en ninguna startup'
            # }),
            "grado_instruccion": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Grado de instrucción",
                }
            ),
            "universidad": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Universidad",
                }
            ),
            "facultad": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Facultad",
                }
            ),
            "escuela": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Escuela",
                }
            ),
            "sectores_interes": forms.Textarea(
                attrs={
                    "class": "w-full h-auto p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none",
                    "rows": 5,
                    "name": "sectores_interes",
                    "id": "sectores_interes",
                    "placeholder": "Escribe los sectores que te interesan, separa por comas.",
                }
            ),
            "habilidades_blandas": forms.Textarea(
                attrs={
                    "class": "w-full h-auto p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none",
                    "rows": 5,
                    "name": "habilidades_blandas",
                    "id": "habilidades_interes",
                    "placeholder": "Escribe las habilidades blandas que posees, separa por comas.",
                }
            ),
        }


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = (
            "biografia",
            "especialidad",
            "profesion",
            "empresa_a_cargo",
            "pertenece_universidad",
            "beneficios",
            "disponibilidad",
            "sala_virtual",
            "mentoria_startups",
            "programa",
        )
        widgets = {
            "biografia": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "rows": 5,
                    "placeholder": "Escribe aquí tu biografía...",
                }
            ),
            "especialidad": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Especialidad",
                }
            ),
            "beneficios": forms.Textarea(
                attrs={
                    "class": "w-full h-auto p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none",
                    "rows": 5,
                    "name": "beneficios",
                    "id": "beneficios",
                    "placeholder": "Escribe los beneficios, uno por línea...",
                }
            ),
            "profesion": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Profesión",
                }
            ),
            "empresa_a_cargo": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500",
                    "placeholder": "Empresa",
                }
            ),
            "pertenece_universidad": forms.CheckboxInput(
                attrs={
                    "class": "hidden",
                    "id": "toggle_pertenece_universidad",
                }
            ),
            "sala_virtual": forms.URLInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500 text-blue-gray-400",
                    "placeholder": "URL de su sala virtual",
                }
            ),
            "disponibilidad": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500 text-blue-gray-400",
                    "placeholder": "Disponibilidad",
                }
            ),
            "Programa": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500 text-blue-gray-400",
                    "placeholder": "Programa",
                }
            ),
        }


class AdminMentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ["puede_cobrar", "precio_por_hora"]

    def clean(self):
        cleaned_data = super().clean()
        puede_cobrar = cleaned_data.get("puede_cobrar")
        precio_por_hora = cleaned_data.get("precio_por_hora")

        if puede_cobrar and not precio_por_hora:
            raise forms.ValidationError(
                "Debe especificar un precio por hora si se habilita el cobro."
            )

        return cleaned_data


class SolicitudMentoriaForm(forms.ModelForm):
    class Meta:
        model = Mentoria
        fields = ["fecha", "temas"]  # mentor,
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop("startup", None)
        super(SolicitudMentoriaForm, self).__init__(*args, **kwargs)

        # Filtra los mentores que están en el mismo programa que la startup

    #  if startup and startup.programa:
    #     self.fields['mentor'].queryset = Mentor.objects.filter(programa=startup.programa)
    # else:
    #   self.fields['mentor'].queryset = Mentor.objects.none()  # Evita mostrar mentores si no hay programa


class EditarMentoriaForm(forms.ModelForm):
    class Meta:
        model = Mentoria
        fields = ["temas", "fecha", "estado"]
        widgets = {
            "temas": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Temas a tratar"}
            ),
            "fecha": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "value": lambda instance: (
                        instance.fecha.strftime("%Y-%m-%dT%H:%M")
                        if instance and instance.fecha
                        else ""
                    ),
                }
            ),
        }
