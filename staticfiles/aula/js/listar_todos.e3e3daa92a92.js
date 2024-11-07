document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');
     // Variables globales
     let currentTab = 'emprendedores';
     let searchQuery = '';
     let currentPage = 1;

     // Función para obtener el valor de una cookie
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

    // Función para cargar el contenido de una pestaña
    function loadTabContent(tab, page = 1) {
        const url = `/comunidad/?tab=${tab}&search=${encodeURIComponent(searchQuery)}&page=${page}`;
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('tab-content').innerHTML = data.html;
            currentTab = tab;
            currentPage = page;
            updatePlaceholder(tab);
            setupEventHandlers();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Función para cambiar el placeholder según la pestaña activa
    function updatePlaceholder(tabName) {
        const searchInput = document.getElementById('search-input');
        switch(tabName) {
            case 'emprendedores':
                searchInput.placeholder = 'Buscar emprendedor';
                break;
            case 'mentores':
                searchInput.placeholder = 'Buscar mentor';
                break;
            case 'startups':
                searchInput.placeholder = 'Buscar startup';
                break;
            default:
                searchInput.placeholder = 'Buscar';
        }
    }

    // Evento para cambiar de pestaña
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            // Actualizar estilos de los botones
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('bg-blue-500', 'text-white'));
            this.classList.add('bg-blue-500', 'text-white');
            // Reiniciar la búsqueda
            searchQuery = '';
            document.getElementById('search-input').value = '';
            // Cargar contenido de la pestaña
            loadTabContent(tab);
        });
    });
    
    // Evento para manejar el cambio en el campo de búsqueda
    document.getElementById('search-input').addEventListener('input', function(event) {
        searchQuery = event.target.value;
        if (searchQuery === '') {
            // Si el campo de búsqueda está vacío, cargar todos los resultados
            loadTabContent(currentTab);
        }
    });

    // Función debounce
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }

    // Evento para manejar el cambio en el campo de búsqueda con debounce
    const debouncedSearch = debounce(function(event) {
        searchQuery = event.target.value;
        loadTabContent(currentTab);
    }, 300); // Espera 300ms después de que el usuario deja de escribir

    document.getElementById('search-input').addEventListener('input', debouncedSearch);

    // Evento para manejar la paginación
    document.getElementById('tab-content').addEventListener('click', function(event) {
        if (event.target.classList.contains('pagination-btn')) {
            const page = event.target.getAttribute('data-page');
            loadTabContent(currentTab, page);
        }
    });

    // Cargar la pestaña inicial
    loadTabContent(currentTab);

     // Funciones existentes para cancelar mentorías y dejar de seguir startups
    // Ajustadas para funcionar con el contenido dinámico

    function setupEventHandlers() {
        // Cancelar Mentorías
        document.querySelectorAll('.cancelar-mentoria').forEach(button => {
            button.addEventListener('click', function() {
                const mentoriaId = this.getAttribute('data-mentoria-id');
                if (confirm('¿Estás seguro de que quieres cancelar esta mentoría?')) {
                    fetch(`/cancelar-mentoria/${mentoriaId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Mentoría cancelada con éxito.');
                            loadTabContent(currentTab, currentPage);
                        } else {
                            alert('Error al cancelar la mentoría: ' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Ocurrió un error al cancelar la mentoría.');
                    });
                }
            });
        });

        // Dejar de Seguir Startup
        document.querySelectorAll('.dejar-seguir-startup').forEach(button => {
            button.addEventListener('click', function() {
                const seguimiento_id = this.getAttribute('data-seguimiento-id');
                if (confirm('¿Estás seguro de que quieres dejar de seguir esta startup?')) {
                    fetch(`/dejar-seguir-startup/${seguimiento_id}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Has dejado de seguir la startup con éxito.');
                            loadTabContent(currentTab, currentPage);
                        } else {
                            alert('Error al dejar de seguir la startup: ' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Ocurrió un error al dejar de seguir la startup.');
                    });
                }
            });
        });
    }
    


});
