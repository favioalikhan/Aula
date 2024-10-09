from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from wagtail.models import Page
from .models import ProgramaPage, Startup
from .forms import StartupForm

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Check if home page already exists
        home_page = Page.objects.filter(slug="home", depth=2).first()
        if not home_page:
            # If it doesn't exist, create it
            self.home_page = self.root_page.add_child(
                instance=Page(
                    title="Home",
                    slug="home",
                    content_type=self.root_page.content_type,
                    path="00010001",
                    depth=2,
                    numchild=0,
                    url_path="/home/",
                )
            )
        else:
            # If it exists, use it
            self.home_page = home_page


class InscribirStartupUnitTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="12345"
        )
        self.programa = ProgramaPage(
            title="Test Programa",
            titulo="Test Programa",  # Asegúrate de que 'titulo' no esté vacío
        )
        self.home_page.add_child(instance=self.programa)
        self.startup = Startup.objects.create(nombre="Test Startup", fundador=self.user)


class CrearStartupUnitTest(TestCase):
    def test_formulario_startup_valido(self):
        form_data = {"nombre": "Mi Startup", "descripcion": "Una descripción"}
        form = StartupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_startup_invalido(self):
        form_data = {"nombre": "", "descripcion": "Descripción sin nombre"}
        form = StartupForm(data=form_data)
        self.assertFalse(form.is_valid())


class IntegracionStartupTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="12345"
        )
        self.startup = Startup.objects.create(nombre="Test Startup", fundador=self.user)
        self.client.login(username="testuser", password="12345")


class SistemaStartupTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="12345"
        )
        self.startup = Startup.objects.create(
            nombre="Sistema Startup", fundador=self.user
        )
        self.programa = ProgramaPage(
            title="Programa del Sistema", titulo="Programa del Sistema"
        )  # Add 'titulo' here
        self.home_page.add_child(instance=self.programa)
        self.client.login(username="testuser", password="12345")

    def test_inscripcion_y_creacion_de_startup(self):
        crear_startup_data = {
            "nombre": "Nueva Sistema Startup",
            "descripcion": "Descripción del sistema",
        }
        response = self.client.post(reverse("crear_startup"), crear_startup_data)
        self.assertEqual(response.status_code, 302)

        inscribir_startup_data = {"programa_id": self.programa.id}
        response = self.client.post(
            reverse("inscribir_startup", args=[self.programa.id]),
            inscribir_startup_data,
        )
        self.assertEqual(response.status_code, 302)
        self.startup.refresh_from_db()
        self.assertEqual(self.startup.programa, self.programa)


class AceptacionStartupTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="acceptuser", email="acceptuser@example.com", password="12345"
        )
        self.startup = Startup.objects.create(
            nombre="Aceptación Startup", fundador=self.user
        )
        self.client.login(username="acceptuser", password="12345")

    def test_crear_y_ver_perfil_de_startup(self):
        response = self.client.get(reverse("profile-startup"))
        self.assertEqual(response.status_code, 302)  # Asumimos que redirige
        response = self.client.get(reverse("profile-startup"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aceptación Startup")

    def test_crear_startup_sin_startup_asociada(self):
        self.programa = ProgramaPage(title="Test Programa")
        self.home_page.add_child(instance=self.programa)
        self.assertTrue(ProgramaPage.objects.filter(title="Test Programa").exists())
