from django.test import TestCase
from django.core.exceptions import ValidationError
from usuarios.models import CustomUser, SeguidorStartup, Startup
from programa_startup.models import ProgramaPage
from wagtail.models import Page


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para crear un usuario
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="securepassword123",
            rol=CustomUser.EMPRENDEDOR,
        )

    def test_create_user(self):
        # Verifica que el usuario se ha creado correctamente
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.rol, CustomUser.EMPRENDEDOR)

    def test_create_superuser(self):
        # Verifica que el superusuario tiene los permisos adecuados
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="adminuser",
            password="supersecurepassword",
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.rol, CustomUser.ADMINISTRADOR)

    def test_clean_username(self):
        # Verifica que el nombre de usuario no pueda contener números
        self.user.username = "user123"
        with self.assertRaises(ValidationError):
            self.user.clean_username()

    def test_save_user_with_profile_creation(self):
        # Verifica que al guardar un usuario emprendedor, se crea el perfil de emprendedor automáticamente
        self.assertTrue(hasattr(self.user, "emprendedor_profile"))


class EmprendedorModelTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para crear un emprendedor
        self.user = CustomUser.objects.create_user(
            email="emprendedor@example.com",
            username="emprendedor1",
            password="securepassword",
            rol=CustomUser.EMPRENDEDOR,
        )
        self.emprendedor = self.user.emprendedor_profile

    def test_emprendedor_creation(self):
        # Verifica que el perfil de emprendedor se haya creado correctamente
        self.assertEqual(self.emprendedor.user, self.user)
        self.assertIsNone(self.emprendedor.startup)


class MentorModelTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para crear un mentor
        self.user = CustomUser.objects.create_user(
            email="mentor@example.com",
            username="mentor1",
            password="securepassword",
            rol=CustomUser.MENTOR,
        )
        root_page = Page.objects.get(id=1)
        self.programa = ProgramaPage(
            titulo="Programa de Mentoría",
            title="Programa de Mentoría",
            slug="programa-de-mentoria",
            descripcion="Descripción del programa",
        )
        root_page.add_child(instance=self.programa)
        self.programa.save_revision().publish()
        self.mentor = self.user.mentor_profile
        self.mentor.programa = self.programa
        self.mentor.save()

    def test_mentor_creation(self):
        # Verifica que el perfil de mentor se haya creado correctamente
        self.assertEqual(self.mentor.user, self.user)
        self.assertEqual(self.mentor.programa, self.programa)

    def test_mentoria_gratis(self):
        # Verifica que la mentoría sea gratuita si no tiene precio por hora asignado
        self.assertTrue(self.mentor.es_mentoria_gratis())
        self.mentor.precio_por_hora = 50.00
        self.mentor.puede_cobrar = True
        self.mentor.save()
        self.assertFalse(self.mentor.es_mentoria_gratis())


class SeguidorStartupModelTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para crear un emprendedor y una startup
        self.user = CustomUser.objects.create_user(
            email="seguidor@example.com",
            username="seguidor1",
            password="securepassword",
            rol=CustomUser.EMPRENDEDOR,
        )
        self.emprendedor = self.user.emprendedor_profile
        self.startup = Startup.objects.create(
            nombre="Startup Ejemplo",
            fundador=self.emprendedor.user,  # Añadir el fundador
        )

    def test_seguir_startup(self):
        # Verifica que un emprendedor pueda seguir una startup
        seguidor = SeguidorStartup.objects.create(
            usuario=self.emprendedor, startup=self.startup
        )
        self.assertEqual(seguidor.usuario, self.emprendedor)
        self.assertEqual(seguidor.startup, self.startup)

    def test_limite_seguimiento_startups(self):
        # Verifica que un emprendedor no pueda seguir más de 5 startups
        for i in range(5):
            startup = Startup.objects.create(
                nombre=f"Startup {i}",
                fundador=self.emprendedor.user,  # Añadir el fundador
            )
            SeguidorStartup.objects.create(usuario=self.emprendedor, startup=startup)
        nueva_startup = Startup.objects.create(
            nombre="Startup Nueva",
            fundador=self.emprendedor.user,  # Añadir el fundador
        )
        with self.assertRaises(ValidationError):
            SeguidorStartup.objects.create(
                usuario=self.emprendedor, startup=nueva_startup
            )
