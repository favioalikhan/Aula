document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');
    
    const marcarTodasLeidasBtn = document.getElementById('marcar-todas-leidas');
    const eliminarTodasBtn = document.getElementById('eliminar-todas');
    // Función para marcar todas las notificaciones como leídas
    if (marcarTodasLeidasBtn) {
        marcarTodasLeidasBtn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres marcar todas las notificaciones como leídas?')) {
                fetch('/notificaciones/marcar-todas-leidas/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    if (response.ok) {
                        mostrarMensaje('Todas las notificaciones han sido marcadas como leídas.');
                        // Aquí puedes refrescar la lista de notificaciones o hacer algo adicional
                        location.reload();
                    } else {
                        mostrarMensaje('Error al marcar como leídas.');
                    }
                })
                .catch(error => {
                    mostrarMensaje('Error en la solicitud.');
                });
            }
        });
    }

    if (eliminarTodasBtn) {
        // Función para eliminar todas las notificaciones
        eliminarTodasBtn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres eliminar todas las notificaciones?')) {
                fetch('/notificaciones/eliminar-todas/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    if (response.ok) {
                        mostrarMensaje('Todas las notificaciones han sido eliminadas.');
                        location.reload();
                    } else {
                        mostrarMensaje('Error al eliminar las notificaciones.');
                    }
                })
                .catch(error => {
                    mostrarMensaje('Error en la solicitud.');
                });
            }
        });
    }

    // Función para mostrar un mensaje en pantalla
    function mostrarMensaje(mensaje) {
        const mensajeDiv = document.getElementById('mensaje');
        mensajeDiv.innerHTML = mensaje;
        mensajeDiv.style.display = 'block';
    }

    // Función para obtener el valor de la cookie CSRF
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
});