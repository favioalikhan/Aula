const notificationButton = document.getElementById('notificationButton');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationsContainer = notificationDropdown.querySelector('div[role="none"]');

    const notifications = [
        { id: 1, name: "John Doe", action: "te ha enviado una solicitud de conexión", time: "hace 5 minutos" },
        { id: 2, name: "Jane Smith", action: "ha comentado en tu publicación", time: "hace 10 minutos" },
        { id: 3, name: "Startup Inc.", action: "ha publicado una nueva oferta de trabajo", time: "hace 1 hora" }
    ];

    function toggleDropdown() {
        notificationDropdown.classList.toggle('hidden');
    }

    function renderNotifications() {
        notificationsContainer.innerHTML = notifications.map(notification => `
            <div class="px-4 py-3 hover:bg-gray-100">
                <p class="text-sm text-gray-900"><strong>${notification.name}</strong> ${notification.action}</p>
                <p class="text-xs text-gray-500">${notification.time}</p>
            </div>
        `).join('');
    }

    notificationButton.addEventListener('click', () => {
        toggleDropdown();
        renderNotifications();
    });

    // Código existente para el menú móvil
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const programasToggle = document.getElementById('programas-toggle');
    const programasSubmenu = document.getElementById('programas-submenu');

    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('-translate-x-full');
    });

    programasToggle.addEventListener('click', () => {
        programasSubmenu.classList.toggle('hidden');
    });

    // Cerrar el menú móvil cuando se hace clic fuera de él
    document.addEventListener('click', (event) => {
        if (!mobileMenu.contains(event.target) && !menuToggle.contains(event.target)) {
            mobileMenu.classList.add('-translate-x-full');
        }
    });