document.getElementById('buscar-btn').addEventListener('click', function(event) {
    event.preventDefault();
    const query = document.getElementById('search-integrante').value.trim();

    if (query === '') {
        alert('Por favor, ingresa un nombre para buscar.');
        return;
    }

    fetch(`/buscar-integrante/?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultadosDiv = document.getElementById('resultados-busqueda');
            resultadosDiv.innerHTML = '';  // Limpiar resultados anteriores

            if (data.results.length === 0) {
                resultadosDiv.style.display = 'none';  // Ocultar el div si no hay resultados
                resultadosDiv.innerHTML = '<p class="text-gray-600">No se encontraron integrantes.</p>';
            } else {
                resultadosDiv.style.display = 'block';  // Mostrar el div si hay resultados
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
                        showCargoModal(integrante.id, integrante.nombre); // Mostrar el modal para ingresar el cargo
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
    const cargoModal = document.getElementById('cargoModal');
    const saveCargoBtn = document.getElementById('save-cargo-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const cargoInput = document.getElementById('cargo-input');

    cargoModal.classList.remove('hidden');
    cargoInput.value = '';

    saveCargoBtn.onclick = function() {
        const cargo = cargoInput.value.trim();
        if (!cargo) {
            alert('El cargo no puede estar vacío.');
            return;
        }
        agregarIntegrante(id, nombre, cargo); // Pasar el cargo al agregar el integrante
        cargoModal.classList.add('hidden');
    };

    cancelBtn.onclick = function() {
        cargoModal.classList.add('hidden');
    };
}

function agregarIntegrante(id, nombre, cargo) { // Añadir el parámetro 'cargo'
    const integrantesLista = document.getElementById('integrantes-lista');
    
    // Verificar si el integrante ya está en la lista
    const integrantesItems = integrantesLista.querySelectorAll('li');
    for (let item of integrantesItems) {
        if (item.dataset.id === id) {
            alert('Este integrante ya está en la lista.');
            return; // No agregar el mismo integrante si ya está en la lista
        }
    }
    
    const integranteItem = document.createElement('li');
    integranteItem.textContent = `${nombre} - Cargo: ${cargo}`; // Incluir el cargo en el texto
    integranteItem.classList.add('flex', 'items-center', 'justify-between', 'p-2', 'border', 'border-gray-300', 'rounded-md', 'mb-2');
    integranteItem.dataset.id = id;
    
    // Crear un campo input oculto para enviar el ID y cargo del integrante
    const integranteInput = document.createElement('input');
    integranteInput.type = 'hidden';
    integranteInput.name = 'integrantes';
    integranteInput.value = `${id}:${cargo}`;
    
    integranteItem.appendChild(integranteInput); // Añadir el input al item de la lista
    
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
    const resultadosDiv = document.getElementById('resultados-busqueda');
    resultadosDiv.innerHTML = '';
    resultadosDiv.style.display = 'none';
}
