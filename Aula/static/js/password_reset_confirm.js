document.addEventListener('DOMContentLoaded', function () {
    // Funcionalidad de alternar visibilidad de contraseñas
    const togglePassword1 = document.querySelector('#togglePassword1');
    const password1 = document.querySelector('#id_new_password1');
    const toggleIcon1 = document.querySelector('#toggleIcon1');

    if (togglePassword1 && password1 && toggleIcon1) {
        togglePassword1.addEventListener('click', function() {
            const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
            password1.setAttribute('type', type);
            
            toggleIcon1.className = type === 'password' ? 'fa-light fa-eye-slash' : 'fa-sharp fa-light fa-eye';
        });
    }
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#id_new_password2');
    const toggleIcon2 = document.querySelector('#toggleIcon2');

    if (togglePassword2 && password2 && toggleIcon2) {
        togglePassword2.addEventListener('click', function() {
            const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
            password2.setAttribute('type', type);
            
            toggleIcon2.className = type === 'password' ? 'fa-light fa-eye-slash' : 'fa-sharp fa-light fa-eye';
        });
    }
    });