document.addEventListener('DOMContentLoaded', function () {
    // Funcionalidad de alternar visibilidad de contraseñas
    const togglePassword1 = document.querySelector('#togglePassword1');
    const password1 = document.querySelector('#password1');
    const toggleIcon1 = document.querySelector('#toggleIcon1');

    if (togglePassword1 && password1 && toggleIcon1) {
        togglePassword1.addEventListener('click', function() {
            const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
            password1.setAttribute('type', type);
            
            toggleIcon1.className = type === 'password' ? 'fa-light fa-eye-slash' : 'fa-sharp fa-light fa-eye';
        });
    }

    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');
    const toggleIcon2 = document.querySelector('#toggleIcon2');

    if (togglePassword2 && password2 && toggleIcon2) {
        togglePassword2.addEventListener('click', function() {
            const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
            password2.setAttribute('type', type);
            
            toggleIcon2.className = type === 'password' ? 'fa-light fa-eye-slash' : 'fa-sharp fa-light fa-eye';
        });
    }



    const roleModal = document.getElementById('roleModal');
    const successModal = document.getElementById('successModal');
    const roleTitle = document.getElementById('roleTitle');
    const roleInput = document.getElementById('rol');
    const registrationForm = document.getElementById('registrationForm');
    const errorAlert = document.querySelector('.bg-red[role="alert"]'); // Selecciona la alerta de error
  
    // Oculta el modal de selección de rol por defecto
    roleModal.classList.add('hidden');
  
    // Si hay una alerta de error, agregar temporizador para cerrarla después de 5 segundos
    if (errorAlert) {
        setTimeout(function () {
            errorAlert.classList.add('hidden'); // Oculta la alerta
            openRoleModal(); // Vuelve a mostrar el modal de selección de rol después de la alerta
        }, 5000);
    } else {
        // Si no hay alerta de error, mostrar el modal de selección de rol de inmediato
        openRoleModal();
    }
  
    // Manejo de la selección del rol
    document.querySelectorAll('#roleModal button').forEach(button => {
        button.addEventListener('click', function () {
            const selectedRole = this.getAttribute('data-role');
            roleTitle.innerText = `Conviértete en ${selectedRole.toLowerCase()}`;
            roleInput.value = selectedRole;
            closeRoleModal(); // Cierra el modal de selección de rol
        });
    });
  
    // Manejo del envío del formulario y apertura del modal de éxito
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            event.preventDefault();
            openSuccessModal();
        });
    }
  
    // Función para abrir el modal de éxito
    function openSuccessModal() {
        successModal.classList.remove('hidden');
        
        // Cierra el modal automáticamente después de 3 segundos y redirige al login
        setTimeout(function() {
            closeSuccessModal();
            window.location.href = "{% url 'login' %}"; // Redirige al login
        }, 3000);
    }
  
    // Función para cerrar el modal de éxito
    function closeSuccessModal() {
        successModal.classList.add('hidden');
    }
  
    // Funciones para abrir y cerrar el modal de rol
    function openRoleModal() {
        roleModal.classList.remove('hidden');
    }
  
    function closeRoleModal() {
        roleModal.classList.add('hidden');
    }
  
    // Asegurar que las funciones estén disponibles globalmente
    window.closeSuccessModal = closeSuccessModal;
    window.openRoleModal = openRoleModal;
    window.closeRoleModal = closeRoleModal;
});
