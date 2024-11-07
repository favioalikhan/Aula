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

    // Código para manejar la búsqueda y adición de nuevos integrantes
    const buscarBtn = document.getElementById('buscar-btn');
    const searchInput = document.getElementById('search-integrante');
    const resultadosDiv = document.getElementById('resultados-busqueda');
    const integrantesLista = document.getElementById('integrantes-lista');
    const cargoModal = document.getElementById('cargoModal');
    const cargoInput = document.getElementById('cargo-input');
    const saveCargoBtn = document.getElementById('save-cargo-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    buscarBtn.addEventListener('click', function(event) {
        event.preventDefault();
        const query = searchInput.value.trim();
    
        if (query === '') {
            alert('Por favor, ingresa un nombre para buscar.');
            return;
        }
    
        fetch(`/buscar-integrante/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultadosDiv.innerHTML = '';  // Limpiar resultados anteriores
    
                if (data.results.length === 0) {
                    resultadosDiv.style.display = 'none';
                    resultadosDiv.innerHTML = '<p class="text-gray-600">No se encontraron integrantes.</p>';
                } else {
                    resultadosDiv.style.display = 'block';
                    data.results.forEach(function(integrante) {
                        const integranteDiv = document.createElement('div');
                        integranteDiv.classList.add('flex', 'items-center', 'justify-between', 'p-2', 'border', 'border-gray-300', 'rounded-md', 'mb-2');
                        
                        const nombreSpan = document.createElement('span');
                        nombreSpan.textContent = integrante.nombre;
                        nombreSpan.classList.add('flex-1');
                        
                        const agregarBtn = document.createElement('button');
                        agregarBtn.textContent = 'Agregar';
                        agregarBtn.type = 'button';
                        agregarBtn.classList.add('bg-blue-600', 'text-white', 'px-3', 'py-1', 'rounded-md', 'hover:bg-blue-700', 'focus:outline-none', 'focus:ring-2', 'focus:ring-offset-2', 'focus:ring-blue-500');
                        agregarBtn.addEventListener('click', function(event) {
                            event.preventDefault();
                            showCargoModal(integrante.id, integrante.nombre);
                        });
    
                        integranteDiv.appendChild(nombreSpan);
                        integranteDiv.appendChild(agregarBtn);
                        resultadosDiv.appendChild(integranteDiv);
                    });
                }
            })
            .catch(error => {
                console.error('Error al buscar integrantes:', error);
                alert('Ocurrió un error al buscar el integrante. Por favor, inténtelo de nuevo.');
            });
    });

    function showCargoModal(id, nombre) {
        cargoModal.classList.remove('hidden');
        cargoInput.value = '';
    
        saveCargoBtn.onclick = function() {
            const cargo = cargoInput.value.trim();
            if (!cargo) {
                alert('El cargo no puede estar vacío.');
                return;
            }
            agregarIntegrante(id, nombre, cargo);
            cargoModal.classList.add('hidden');
        };
    
        cancelBtn.onclick = function() {
            cargoModal.classList.add('hidden');
        };
    }
    
    function agregarIntegrante(id, nombre, cargo) {
        // Verificar si el integrante ya está en la lista
        const integrantesItems = integrantesLista.querySelectorAll('li');
        for (let item of integrantesItems) {
            if (item.dataset.id === id) {
                alert('Este integrante ya está en la lista.');
                return;
            }
        }
        
        const integranteItem = document.createElement('li');
        integranteItem.textContent = `${nombre} - Cargo: ${cargo}`;
        integranteItem.classList.add('flex', 'items-center', 'justify-between', 'p-2', 'border', 'border-gray-300', 'rounded-md', 'mb-2');
        integranteItem.dataset.id = id;
        
        const integranteInput = document.createElement('input');
        integranteInput.type = 'hidden';
        integranteInput.name = 'integrantes';
        integranteInput.value = `${id}:${cargo}`;
        
        integranteItem.appendChild(integranteInput);
        
        const eliminarBtn = document.createElement('button');
        eliminarBtn.textContent = 'Eliminar';
        eliminarBtn.type = 'button';
        eliminarBtn.classList.add('bg-red', 'text-white', 'px-3', 'py-1', 'rounded-md', 'hover:bg-red-700', 'focus:outline-none', 'focus:ring-2', 'focus:ring-offset-2', 'focus:ring-red-500');
        eliminarBtn.addEventListener('click', function(event) {
            event.preventDefault();
            integranteItem.remove();
        });
    
        integranteItem.appendChild(eliminarBtn);
        integrantesLista.appendChild(integranteItem);
        
        // Limpiar y ocultar el div de resultados después de agregar el integrante
        resultadosDiv.innerHTML = '';
        resultadosDiv.style.display = 'none';
    }

    const csrftoken = getCookie('csrftoken');

    function eliminarIntegrante(integranteId) {
        if (confirm('¿Estás seguro de que deseas eliminar este integrante?')) {
            fetch(`/eliminar-integrante/${integranteId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    // Eliminar el elemento del DOM
                    const integranteElement = document.querySelector(`[data-integrante-id="${integranteId}"]`).closest('.flex');
                    integranteElement.remove();
                } else {
                    throw new Error('Error al eliminar el integrante');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al eliminar el integrante. Por favor, inténtelo de nuevo.');
            });
        }
    }

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
                        // Intentar eliminar la mentoría de la interfaz
                        const mentoriaElement = document.getElementById(`mentoria-${mentoriaId}`);
                        if (mentoriaElement) {
                            mentoriaElement.remove();
                        } else {
                            console.warn(`Elemento con ID mentoria-${mentoriaId} no encontrado`);
                        }

                        // Verificar si no quedan más mentorías
                        const mentoriasContainer = document.querySelector('#mentoria .space-y-4');
                        if (mentoriasContainer && !mentoriasContainer.querySelector('.flex')) {
                            mentoriasContainer.innerHTML = '<p id="no-mentorias">No hay mentorías asociadas a esta startup.</p>';
                        }

                        // Si el botón aún existe, eliminarlo
                        this.remove();
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

    // Agregar event listeners a los botones de eliminar
    document.querySelectorAll('.eliminar-integrante').forEach(button => {
        button.addEventListener('click', function() {
            const integranteId = this.getAttribute('data-integrante-id');
            eliminarIntegrante(integranteId);
        });
    });

    const abrirModalLogro = document.getElementById('abrir-modal-logro');
    const modalNuevoLogro = document.getElementById('modal-nuevo-logro');
    const cerrarModalLogro = document.getElementById('cerrar-modal-logro');
    const agregarLogro = document.getElementById('agregar-logro');
    const logrosLista = document.getElementById('logros-lista');
    const noLogrosMsg = document.getElementById('no-logros-msg'); 
    

    if (abrirModalLogro && modalNuevoLogro && cerrarModalLogro && agregarLogro) {
        abrirModalLogro.addEventListener('click', function() {
            modalNuevoLogro.classList.remove('hidden');
        });

        cerrarModalLogro.addEventListener('click', function() {
            modalNuevoLogro.classList.add('hidden');
        });

        agregarLogro.addEventListener('click', function() {
            // Aquí puedes agregar la lógica para enviar el formulario
            const titulo = document.getElementById('{{ logro_form.titulo.id_for_label }}').value;
            const descripcion = document.getElementById('{{ logro_form.descripcion.id_for_label }}').value;
            const fecha = document.getElementById('{{ logro_form.fecha_logro.id_for_label }}').value;

            if (!titulo || !descripcion || !fecha) {
                alert('Por favor, completa todos los campos del logro.');
                return;
            }

            const nuevoLogro = document.createElement('div');
            nuevoLogro.classList.add('p-4', 'bg-gray-100', 'rounded-lg', 'shadow-md');
            nuevoLogro.dataset.logroId = "temp_id";
            nuevoLogro.innerHTML = `
            <div class="logro-item">
                <input type="hidden" name="nuevo_logro_ids" value="temp_id"> <!-- Aquí podrías usar un contador -->
                <div>
                    <label for="nuevo_titulo" class="block text-sm font-medium text-gray-700">Título:</label>
                    <input type="text" id="nuevo_titulo" name="nuevo_titulo" value="${titulo}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                </div>
                <div class="mt-2">
                    <label for="nueva_descripcion" class="block text-sm font-medium text-gray-700">Descripción:</label>
                    <textarea id="nueva_descripcion" name="nueva_descripcion" rows="7" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">${descripcion}</textarea>
                </div>
                <div class="mt-2">
                    <label for="nueva_fecha_logro" class="block text-sm font-medium text-gray-700">Fecha:</label>
                    <input type="date" id="nueva_fecha_logro" name="nueva_fecha_logro" value="${fecha}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                </div>
                <div class="mt-2">
                    <label class="hidden inline-flex items-center">
                        <input type="checkbox" name="eliminar_logro_temp_id" class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                        <span class="eliminar-logro ml-2 text-sm text-gray-600">Eliminar este logro</span>
                    </label>
                    <button type="button" class="eliminar-logro-btn bg-red text-white px-2 py-1 rounded">Eliminar Logro</button>
                </div>
            </div>
            `;

            // Agregar el nuevo logro a la lista
            logrosLista.appendChild(nuevoLogro);

            
            // Opcional: Limpiar los campos del formulario
             document.getElementById('{{ logro_form.titulo.id_for_label }}').value = '';
             document.getElementById('{{ logro_form.descripcion.id_for_label }}').value = '';
             document.getElementById('{{ logro_form.fecha_logro.id_for_label }}').value = '';
             modalNuevoLogro.classList.add('hidden');
            
             // Agregar evento para eliminar el logro
             nuevoLogro.querySelector('.eliminar-logro-btn').addEventListener('click', function() {
                nuevoLogro.remove();
            });

            if (logrosLista.children.length > 1) {
                noLogrosMsg.classList.add('hidden');
            }
        });

        logrosLista.addEventListener('click', function(e) {
            if (e.target.classList.contains('eliminar-logro-btn')) {
                const logroItem = e.target.closest('.logro-item');
                const checkbox = logroItem.querySelector('input[type="checkbox"][name^="eliminar_logro_"]');
                if (checkbox) {
                    checkbox.checked = true;
                    logroItem.style.opacity = 0.5; // Opcional: Indicar visualmente que está marcado para eliminación
                }
            }
        });

        // Cerrar el modal si se hace clic fuera de él
        window.addEventListener('click', function(event) {
            if (event.target === modalNuevoLogro) {
                modalNuevoLogro.classList.add('hidden');
            }
        });
    }
});