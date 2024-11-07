from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import CustomUser


class TemplateUsageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = "securepassword123"
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password=self.user_password,
            rol=CustomUser.EMPRENDEDOR,
        )

        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.profile_url = reverse("profile")
        self.edit_profile_url = reverse("edit-profile")
        self.delete_account_url = reverse("eliminar-cuenta")
        self.password_reset_url = reverse("password-reset")
        self.password_reset_done_url = reverse("password-reset-done")

    def test_register_template_used(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, "usuarios/register.html")

    def test_login_template_used(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, "usuarios/login.html")

    def test_profile_template_used(self):
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, "usuarios/profile_user.html")

    def test_edit_profile_template_used(self):
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.get(self.edit_profile_url)
        self.assertTemplateUsed(response, "usuarios/edit_profile.html")

    def test_password_reset_template_used(self):
        response = self.client.get(self.password_reset_url)
        self.assertTemplateUsed(response, "usuarios/password_reset_form.html")

    def test_password_reset_done_template_used(self):
        response = self.client.get(self.password_reset_done_url)
        self.assertTemplateUsed(response, "usuarios/password_reset_done.html")

    def test_delete_account_template_used(self):
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.post(self.delete_account_url)
        self.assertTemplateUsed(response, "usuarios/delete_account.html")

    def test_password_reset_confirm_template_used(self):
        # Simulando el enlace de restablecimiento de contraseña con uid y token
        response = self.client.get(
            reverse(
                "password-reset-confirm", kwargs={"uidb64": "uid", "token": "token"}
            )
        )
        self.assertTemplateUsed(response, "usuarios/password_reset_confirm.html")

    def test_password_reset_complete_template_used(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertTemplateUsed(response, "usuarios/password_reset_complete.html")
