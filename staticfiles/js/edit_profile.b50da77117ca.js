document.addEventListener('DOMContentLoaded', function () {
    const toggleCheckbox = document.querySelector('#toggle_pertenece_universidad');
    const toggleIcon = document.querySelector('#toggle-icon');

    function updateToggleIcon() {
        if (toggleCheckbox.checked) {
            toggleIcon.classList.remove('fa-toggle-off', 'text-gray-500');
            toggleIcon.classList.add('fa-toggle-on', 'text-blue-600');
        } else {
            toggleIcon.classList.remove('fa-toggle-on', 'text-blue-600');
            toggleIcon.classList.add('fa-toggle-off', 'text-gray-500');
        }
    }

    // Añadir animación de transición suave al cambio de color y forma del ícono
    toggleIcon.style.transition = 'color 0.3s ease, transform 0.3s ease';

    // Activar el cambio de estado del checkbox al hacer clic en el ícono
    toggleIcon.addEventListener('click', function() {
        toggleCheckbox.checked = !toggleCheckbox.checked;
        updateToggleIcon();
    });

    // Inicializar el estado del ícono del toggle al cargar
    updateToggleIcon();

    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.dejar-seguir-startup').forEach(button => {
        button.addEventListener('click', function() {
            const seguimientoId = this.getAttribute('data-seguimiento-id');
            if (confirm('¿Estás seguro de que quieres dejar de seguir esta startup?')) {
                fetch(`/dejar-seguir-startup/${seguimientoId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Eliminar la startup de la interfaz
                        const seguimientoElement = document.getElementById(`seguimiento-${seguimientoId}`);
                        if (seguimientoElement) {
                            seguimientoElement.remove();
                        }

                        // Verificar si no quedan más startups seguidas
                        const seguimientosContainer = document.querySelector('#startups .space-y-4');
                        if (seguimientosContainer && !seguimientosContainer.querySelector('.flex')) {
                            seguimientosContainer.innerHTML = '<p id="no-seguimientos">No estás siguiendo ninguna startup.</p>';
                        }

                        alert('Has dejado de seguir la startup con éxito.');
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
});


//Prueba
/*document.addEventListener('DOMContentLoaded', function() {
    const editarBtn = document.getElementById('edit-button');
    const actualizarBtn = document.getElementById('update-button');
    const editIcons = document.querySelectorAll('#edit-icon');
    const viewModes = document.querySelectorAll('[id$="-view"]');
    const editModes = document.querySelectorAll('[id$="-edit"]');
    const inputs = document.querySelectorAll('input, select, textarea');
    const fotoView = document.getElementById('foto-view');

    editarBtn.addEventListener('click', function() {
        toggleEditMode(true);
    });

    actualizarBtn.addEventListener('click', function(event) {
        toggleEditMode(false);
    });

    function toggleEditMode(editing) {
        editarBtn.classList.toggle('hidden', editing);
        actualizarBtn.classList.toggle('hidden', !editing);

        editIcons.forEach(icon => {
            icon.classList.toggle('hidden', !editing);
        });

        viewModes.forEach(view => {
            view.classList.toggle('hidden', editing);
        });

        editModes.forEach(edit => {
            edit.classList.toggle('hidden', !editing);
        });

        inputs.forEach(input => {
            input.disabled = !editing;
            if (editing) {
                input.classList.remove('text-blue-gray-400');
                input.classList.add('text-navy-blue');
            } else {
                input.classList.add('text-blue-gray-400');
                input.classList.remove('text-navy-blue');
            }
        });
        if (fotoView) {
            fotoView.classList.toggle('hidden', !editing);
        }
    }
}); */
