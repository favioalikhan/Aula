document.getElementById('agregarIntegranteBtn').addEventListener('click', function() {
    document.getElementById('integranteModal').style.display = 'block';
});

document.getElementById('buscarUsuarioInput').addEventListener('keyup', function() {
    let term = this.value;

    if (term.length > 2) {
        fetch(`/buscar-usuario/?term=${term}`)
            .then(response => response.json())
            .then(data => {
                let resultados = document.getElementById('resultadosBusqueda');
                resultados.innerHTML = '';
                data.results.forEach(usuario => {
                    let li = document.createElement('li');
                    li.textContent = usuario.text;
                    li.dataset.id = usuario.id;
                    resultados.appendChild(li);
                });
            });
    }
});

document.getElementById('resultadosBusqueda').addEventListener('click', function(e) {
    if (e.target.tagName === 'LI') {
        let usuarioId = e.target.dataset.id;
        let cargo = document.getElementById('cargoInput').value;
        let startupId = '{{ startup.id }}';  // Asegúrate de pasar el ID de la startup correctamente

        fetch('/agregar-integrante/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `usuario_id=${usuarioId}&cargo=${cargo}&startup_id=${startupId}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
           // document.getElementById('integranteModal').style.display = 'none';
            // Opcional: Actualizar la lista de integrantes en la página
        });
    }
});
