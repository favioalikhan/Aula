from django.test import SimpleTestCase
from django.urls import reverse, resolve
from usuarios.views import (
    register,
    profile,
    delete_account,
    ruta_emprendedor,
    SolicitarMentoriaView,
    marcar_mentoria_completada,
    EditProfile,
    CustomLoginView,
    cancelar_mentoria,
    password_reset_request,
)
from usuarios.viewsets import CustomAccountView
from django.contrib.auth import views as auth_views


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)

    def test_profile_url_resolves(self):
        url = reverse("profile")
        self.assertEqual(resolve(url).func, profile)

    def test_delete_account_url_resolves(self):
        url = reverse("eliminar-cuenta")
        self.assertEqual(resolve(url).func, delete_account)

    def test_ruta_emprendedor_url_resolves(self):
        url = reverse("ruta-emprendedor")
        self.assertEqual(resolve(url).func, ruta_emprendedor)

    def test_solicitar_mentoria_url_resolves(self):
        url = reverse("solicitar-mentoria", kwargs={"mentor_id": 1})
        self.assertEqual(resolve(url).func.view_class, SolicitarMentoriaView)

    def test_cancelar_mentoria_url_resolves(self):
        url = reverse("cancelar-mentoria", kwargs={"mentoria_id": 1})
        self.assertEqual(resolve(url).func, cancelar_mentoria)

    def test_marcar_mentoria_completada_url_resolves(self):
        url = reverse("marcar-mentoria-completada")
        self.assertEqual(resolve(url).func, marcar_mentoria_completada)

    def test_edit_profile_url_resolves(self):
        url = reverse("edit-profile")
        self.assertEqual(resolve(url).func.view_class, EditProfile)

    def test_custom_account_url_resolves(self):
        url = reverse("wagtailadmin_account")
        self.assertEqual(resolve(url).func.view_class, CustomAccountView)

    def test_login_url_resolves(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_password_reset_url_resolves(self):
        url = reverse("password-reset")
        self.assertEqual(resolve(url).func, password_reset_request)

    def test_password_reset_done_url_resolves(self):
        url = reverse("password-reset-done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse(
            "password-reset-confirm", kwargs={"uidb64": "uid", "token": "token"}
        )
        self.assertEqual(
            resolve(url).func.view_class, auth_views.PasswordResetConfirmView
        )

    def test_password_reset_complete_url_resolves(self):
        url = reverse("password_reset_complete")
        self.assertEqual(
            resolve(url).func.view_class, auth_views.PasswordResetCompleteView
        )
