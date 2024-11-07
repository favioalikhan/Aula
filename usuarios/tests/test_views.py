from django.test import TestCase, Client, override_settings
from django.urls import reverse
from usuarios.models import CustomUser, Mentoria, Startup
from unittest.mock import patch
from programa_startup.models import Notificacion
from django.utils import timezone
from datetime import timedelta


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    STATIC_URL="/static/",
    MEDIA_URL="/media/",
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)
class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = "securepassword123"
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password=self.user_password,
            rol=CustomUser.EMPRENDEDOR,
        )
        self.emprendedor = self.user.emprendedor_profile
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.profile_url = reverse("profile")
        self.delete_account_url = reverse(
            "eliminar-cuenta"
        )  # Asegúrate de que este nombre coincide con tu URL

    def test_register_view_get(self):
        # Verifica que la página de registro se carga correctamente
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usuarios/register.html")

    def test_register_view_post(self):
        # Verifica que un usuario pueda registrarse correctamente
        response = self.client.post(
            self.register_url,
            {
                "email": "newuser@example.com",
                "username": "newuser",
                "password1": "newsecurepassword",
                "password2": "newsecurepassword",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirige al home tras registrarse
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_profile_view_logged_in(self):
        # Verifica que un usuario logueado pueda acceder a su perfil
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usuarios/profile_user.html")

    def test_profile_view_not_logged_in(self):
        # Verifica que un usuario no autenticado sea redirigido al intentar acceder al perfil
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.login_url}?next={self.profile_url}"
        self.assertRedirects(
            response,
            expected_url,
            fetch_redirect_response=False,  # Añade este parámetro
        )

    def test_delete_account_view(self):
        # Verifica que un usuario autenticado pueda eliminar su cuenta
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.post(self.delete_account_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(email=self.user.email).exists())


class PasswordResetViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="securepassword123",
        )
        self.password_reset_url = reverse(
            "password-reset"
        )  # Asegúrate de que este nombre coincide con tu URL

    @patch(
        "usuarios.views.send_password_reset_email"
    )  # Asegúrate de que el path es correcto
    def test_password_reset_view_post_valid_user(self, mock_send_email):
        # Verifica que la vista de restablecimiento de contraseña funcione correctamente para un usuario válido
        response = self.client.post(self.password_reset_url, {"email": self.user.email})
        self.assertEqual(response.status_code, 302)  # Redirige después del envío
        mock_send_email.assert_called_once()

    def test_password_reset_view_post_invalid_user(self):
        # Verifica que la vista de restablecimiento de contraseña maneje un email no registrado
        response = self.client.post(
            self.password_reset_url, {"email": "invalid@example.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No se encontró ningún usuario con esa dirección de correo electrónico.",
        )


class SolicitarMentoriaViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mentor_user = CustomUser.objects.create_user(
            email="mentor@example.com",
            username="mentor1",
            password="securepassword",
            rol=CustomUser.MENTOR,
        )
        self.emprendedor_user = CustomUser.objects.create_user(
            email="emprendedor@example.com",
            username="emprendedor1",
            password="securepassword",
            rol=CustomUser.EMPRENDEDOR,
        )
        self.emprendedor = self.emprendedor_user.emprendedor_profile
        self.startup = Startup.objects.create(
            nombre="Startup Ejemplo", fundador=self.emprendedor_user
        )
        self.mentor = self.mentor_user.mentor_profile
        self.client.login(email=self.emprendedor_user.email, password="securepassword")
        self.solicitar_mentoria_url = reverse(
            "solicitar-mentoria", kwargs={"mentor_id": self.mentor.id}
        )

    def test_solicitar_mentoria_view_get(self):
        # Verifica que la vista de solicitud de mentoría se cargue correctamente
        response = self.client.get(self.solicitar_mentoria_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programa_startup/solicitar_mentoria.html")
        self.assertEqual(response.context["mentor"], self.mentor)

    def test_solicitar_mentoria_view_post(self):
        # Verifica que se pueda crear una solicitud de mentoría correctamente
        response = self.client.post(
            self.solicitar_mentoria_url,
            {"temas": "Asesoría sobre startups", "startup": self.startup.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Mentoria.objects.filter(startup=self.startup, mentor=self.mentor).exists()
        )


class CancelarMentoriaViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mentor_user = CustomUser.objects.create_user(
            email="mentor@example.com",
            username="mentor1",
            password="securepassword",
            rol=CustomUser.MENTOR,
        )
        self.emprendedor_user = CustomUser.objects.create_user(
            email="emprendedor@example.com",
            username="emprendedor1",
            password="securepassword",
            rol=CustomUser.EMPRENDEDOR,
        )
        self.emprendedor = self.emprendedor_user.emprendedor_profile
        self.startup = Startup.objects.create(
            nombre="Startup Ejemplo", fundador=self.emprendedor_user
        )
        self.mentor = self.mentor_user.mentor_profile
        self.mentoria = Mentoria.objects.create(
            mentor=self.mentor,
            startup=self.startup,
            fecha=timezone.now() + timedelta(days=30),  # Usa timezone-aware datetime
            temas="Asesoría sobre startups",
        )
        self.client.login(email=self.emprendedor_user.email, password="securepassword")
        self.cancelar_mentoria_url = reverse(
            "cancelar-mentoria", args=[self.mentoria.id]
        )

    def test_cancelar_mentoria_view_post(self):
        # Verifica que un emprendedor pueda cancelar una mentoría
        self.client.login(email=self.emprendedor_user.email, password="securepassword")
        # Verificar que la mentoría pertenece al usuario
        self.mentoria.startup = self.startup
        self.mentoria.save()
        response = self.client.post(self.cancelar_mentoria_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})
        self.assertFalse(Mentoria.objects.filter(id=self.mentoria.id).exists())
        # Verificar la notificación al mentor
        self.assertTrue(
            Notificacion.objects.filter(
                usuario=self.mentor_user,
                mensaje=f"La mentoría con la startup '{self.startup.nombre}' ha sido cancelada.",
                tipo="Mentoria",
            ).exists()
        )
