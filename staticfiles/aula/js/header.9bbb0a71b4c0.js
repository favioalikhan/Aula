function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener('DOMContentLoaded', function() {
    
    const notificationButton = document.getElementById('notificationButton');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationsContainer = document.getElementById('notificationsContainer');
    const notificationCount = document.getElementById('notificationCount');

    function toggleDropdown() {
        notificationDropdown.classList.toggle('hidden');
        if (!notificationDropdown.classList.contains('hidden')) {
            fetchNotifications();
        }
    }

    if(isAuthenticated){
        function fetchNotifications() {
            const csrftoken = getCookie('csrftoken');
            fetch('/ver-notificaciones/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Data received:", data);
                notificationsContainer.innerHTML = data.notificaciones_html;
                updateNotificationCount(data.unread_notifications_count);
            })
            .catch(error => {
                console.error('Error:', error);
                notificationsContainer.innerHTML = '<p class="text-sm text-red-500 px-4 py-2">Error al cargar las notificaciones.</p>';
            });
        }
        fetchNotifications();
    }

    function updateNotificationCount(count) {
        notificationCount.textContent = count;
        notificationCount.classList.toggle('hidden', count === 0);
    }

    if (notificationButton) {
        //console.log("Adding click event listener to notification button");  
        notificationButton.addEventListener('click', toggleDropdown);
    }

    setInterval(fetchNotifications, 60000);  // Actualizar cada minuto

    // Código existente para el menú móvil
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const programasToggle = document.getElementById('programas-toggle');
    const programasSubmenu = document.getElementById('programas-submenu');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('-translate-x-full');
        });
    }

    if (programasToggle) {
        programasToggle.addEventListener('click', () => {
            programasSubmenu.classList.toggle('hidden');
        });
    }

    // Cerrar el menú móvil cuando se hace clic fuera de él
    document.addEventListener('click', (event) => {
        if (mobileMenu && !mobileMenu.contains(event.target) && !menuToggle.contains(event.target)) {
            mobileMenu.classList.add('-translate-x-full');
        }
    });
    //fetchNotifications();
});