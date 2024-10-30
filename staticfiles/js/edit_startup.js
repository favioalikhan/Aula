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

    function eliminarIntegrante(integranteId) {
        if (confirm('¿Estás seguro de que deseas eliminar este integrante?')) {
            fetch(`/eliminar-integrante/${integranteId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
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
});