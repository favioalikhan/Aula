from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserAcceptanceTestCase(LiveServerTestCase):
    def setUp(self):
        # Configura el navegador para las pruebas
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        self.base_url = self.live_server_url

    def tearDown(self):
        # Cierra el navegador después de cada prueba
        self.browser.quit()

    def test_user_registration_and_login(self):
        """
        Prueba de registro de usuario y posterior inicio de sesión.
        """
        # Navegar a la página de registro
        self.browser.get(f'{self.base_url}{reverse("register")}')

        # Completar el formulario de registro
        role_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-role='EMPRENDEDOR']")
            )
        )
        role_button.click()
        email_element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "id_email"))
        )
        email_element.send_keys("testuser@example.com")
        self.browser.find_element(By.ID, "id_username").send_keys("testuser")
        self.browser.find_element(By.ID, "id_apellido_paterno").send_keys("Perez")
        self.browser.find_element(By.ID, "id_apellido_materno").send_keys("Gomez")
        self.browser.find_element(By.ID, "id_password1").send_keys("securepassword123")
        self.browser.find_element(By.ID, "id_password2").send_keys("securepassword123")
        self.browser.find_element(By.ID, "id_genero").send_keys("Masculino")
        self.browser.find_element(By.ID, "id_fecha_nacimiento").send_keys("2000-01-01")

        # Enviar el formulario
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

        # Esperar y comprobar que se muestra el modal de éxito
        time.sleep(2)
        success_modal = self.browser.find_element(By.ID, "successModal")
        self.assertTrue(
            success_modal.is_displayed(), "Modal de registro exitoso no mostrado."
        )

        # Navegar a la página de inicio de sesión
        self.browser.get(f'{self.base_url}{reverse("login")}')

        # Completar el formulario de inicio de sesión
        self.browser.find_element(By.ID, "email").send_keys("testuser@example.com")
        self.browser.find_element(By.ID, "password").send_keys("securepassword123")

        # Enviar el formulario
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

        # Comprobar que el usuario haya iniciado sesión
        profile_url = reverse("profile")
        self.browser.get(f"{self.base_url}{profile_url}")
        page_title = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn(
            "Perfil de",
            page_title,
            "El usuario no fue redirigido a la página de perfil.",
        )

    def test_request_mentoria(self):
        """
        Prueba el flujo de solicitud de una mentoría para un usuario registrado.
        """
        # Primero, registramos al usuario
        self.test_user_registration_and_login()

        # Navegar a la página de solicitud de mentoría (se asume que existe un mentor con ID 1)
        self.browser.get(
            f'{self.base_url}{reverse("solicitar-mentoria", kwargs={"mentor_id": 1})}'
        )

        # Completar el formulario de solicitud de mentoría
        self.browser.find_element(By.NAME, "temas").send_keys("Asesoría sobre startups")

        # Enviar el formulario
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

        # Comprobar que la solicitud de mentoría haya sido creada
        time.sleep(2)
        success_message = self.browser.find_element(By.CLASS_NAME, "alert-success").text
        self.assertIn(
            "Solicitud enviada con éxito",
            success_message,
            "La solicitud de mentoría no fue enviada correctamente.",
        )
