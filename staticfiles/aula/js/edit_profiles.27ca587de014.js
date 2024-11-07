document.addEventListener('DOMContentLoaded', function () {
    if(isMentorOrSpeaker){
     // Obtener el elemento toggle y el campo de entrada oculto
     const toggleIcon = document.getElementById('toggle-icon');
     const perteneciaInput = document.querySelector('input[name="pertenece_universidad"]');
 
     // Establecer el estado inicial del toggle basado en el valor del input
     if (perteneciaInput.checked) {
         toggleIcon.classList.remove('fa-toggle-off');
         toggleIcon.classList.add('fa-toggle-on');
         toggleIcon.classList.remove('text-gray-500');
         toggleIcon.classList.add('text-blue-500');
     }
 
     // Agregar el evento click al toggle
     toggleIcon.addEventListener('click', function() {
         // Cambiar el estado del checkbox
         perteneciaInput.checked = !perteneciaInput.checked;
 
         // Actualizar la apariencia del toggle
         if (perteneciaInput.checked) {
             toggleIcon.classList.remove('fa-toggle-off');
             toggleIcon.classList.add('fa-toggle-on');
             toggleIcon.classList.remove('text-gray-500');
             toggleIcon.classList.add('text-blue-500');
         } else {
             toggleIcon.classList.remove('fa-toggle-on');
             toggleIcon.classList.add('fa-toggle-off');
             toggleIcon.classList.remove('text-blue-500');
             toggleIcon.classList.add('text-gray-500');
         }
     });}

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

    document.querySelectorAll('.mark-completed-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const mentoriaId = this.getAttribute('data-mentoria-id');

            fetch('/marcar-mentoria-completada/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mentoria_id: mentoriaId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualiza el estado en la interfaz de usuario sin recargar la página
                    const estadoElement = document.querySelector(`#mentoria-${mentoriaId} .mentoria-estado`);
                    const buttonElement = this;
                    if (estadoElement) {
                        estadoElement.innerText = 'COMPLETADA'; // Cambia el estado visualmente
                    }
                    buttonElement.style.display = 'none';
                    alert('Mentoría marcada como completada.');
                } else {
                    alert(data.error || 'Error al marcar la mentoría.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud.');
            });
        });
    });
    // Función para obtener el CSRF token de las cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Comprueba si esta cookie es la que estamos buscando
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
