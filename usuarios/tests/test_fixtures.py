from django.test import TestCase
from django.core.management import call_command
from usuarios.models import CustomUser


class FixturesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Cargar datos de fixtures desde el archivo usuarios.json
        call_command("loaddata", "tests/fixtures/usuarios.json", verbosity=0)

    def test_fixture_users_exist(self):
        # Verificar si los usuarios del fixture fueron creados correctamente
        user1 = CustomUser.objects.get(pk=1)
        self.assertEqual(user1.email, "testuser1@example.com")
        self.assertEqual(user1.rol, CustomUser.EMPRENDEDOR)

        user2 = CustomUser.objects.get(pk=2)
        self.assertEqual(user2.email, "testuser2@example.com")
        self.assertEqual(user2.rol, CustomUser.MENTOR)

        admin_user = CustomUser.objects.get(pk=3)
        self.assertEqual(admin_user.email, "adminuser@example.com")
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.rol, "ADMIN")

    def test_fixture_user_passwords(self):
        # Verificar que los passwords del fixture estén configurados correctamente
        user1 = CustomUser.objects.get(pk=1)
        self.assertTrue(user1.check_password("password123"))

        user2 = CustomUser.objects.get(pk=2)
        self.assertTrue(user2.check_password("password123"))

        admin_user = CustomUser.objects.get(pk=3)
        self.assertTrue(admin_user.check_password("password123"))

    def test_active_users(self):
        # Verificar si todos los usuarios del fixture están activos
        active_users = CustomUser.objects.filter(is_active=True)
        self.assertEqual(active_users.count(), 3)
