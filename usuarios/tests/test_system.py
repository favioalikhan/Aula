from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from usuarios.models import CustomUser


class SystemTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Crear un usuario para pruebas de inicio de sesión
        self.user_password = "testpassword123"
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password=self.user_password,
            rol=CustomUser.EMPRENDEDOR,
        )

    def test_register_user(self):
        # Prueba del proceso de registro de usuario
        self.driver.get(f"{self.live_server_url}/register/")

        # Llenar el formulario de registro
        self.driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.NAME, "username").send_keys("newuser")
        self.driver.find_element(By.NAME, "apellido_paterno").send_keys(
            "ApellidoPaterno"
        )
        self.driver.find_element(By.NAME, "apellido_materno").send_keys(
            "ApellidoMaterno"
        )
        self.driver.find_element(By.NAME, "password1").send_keys("newsecurepassword")
        self.driver.find_element(By.NAME, "password2").send_keys("newsecurepassword")
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # Verificar redirección al login después del registro
        self.assertIn("login", self.driver.current_url)

    def test_login_user(self):
        # Prueba del proceso de inicio de sesión de usuario
        self.driver.get(f"{self.live_server_url}/login/")

        # Llenar el formulario de login
        self.driver.find_element(By.NAME, "username").send_keys(self.user.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # Verificar redirección al perfil después del login
        self.assertIn("profile", self.driver.current_url)

    def test_delete_account(self):
        # Prueba del proceso de eliminación de cuenta
        self.driver.get(f"{self.live_server_url}/login/")

        # Iniciar sesión
        self.driver.find_element(By.NAME, "username").send_keys(self.user.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # Navegar a la página de eliminación de cuenta
        self.driver.get(f"{self.live_server_url}/delete-account/")
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # Verificar redirección al registro después de eliminar la cuenta
        self.assertIn("register", self.driver.current_url)
