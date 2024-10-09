document.addEventListener('DOMContentLoaded', function () {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');

    // Función para manejar el cambio de pestañas
    function switchTab(tabId) {
        // Ocultar todos los contenidos de las pestañas
        tabContents.forEach(content => content.classList.add('hidden'));

        // Mostrar el contenido de la pestaña seleccionada
        document.getElementById(tabId).classList.remove('hidden');
    }

    // Inicializar la pestaña activa
    const defaultTab = 'modelo'; // Cambia esto si quieres que otra pestaña esté activa por defecto
    switchTab(defaultTab);

    // Manejar clics en las pestañas
    tabLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Obtener el ID de la pestaña a mostrar
            const tabId = this.getAttribute('data-tab');

            // Cambiar la pestaña
            switchTab(tabId);

            // Actualizar los estilos de los enlaces de las pestañas
            tabLinks.forEach(l => {
                l.classList.remove('border-b-2', 'border-blue-500', 'text-blue-600');
                l.classList.add('text-gray-500', 'hover:text-gray-700');
            });
            this.classList.add('border-b-2', 'border-blue-500', 'text-blue-600');
            this.classList.remove('text-gray-500', 'hover:text-gray-700');
        });
    });
});