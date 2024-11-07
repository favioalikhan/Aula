document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los inputs de tipo file dentro de widgets personalizados
    const fileInputs = document.querySelectorAll('.custom-image-widget input[type="file"]');

    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Verificar si el archivo es una imagen
                if (!file.type.startsWith('image/')) {
                    mostrarMensajeError(input, 'Por favor, selecciona un archivo de imagen válido.');
                    input.value = ''; // Resetear el input
                    return;
                }

                // Verificar el tamaño del archivo (máximo 10MB)
                const maxSizeMB = 10;
                const maxSizeBytes = maxSizeMB * 1024 * 1024;
                if (file.size > maxSizeBytes) {
                    mostrarMensajeError(input, `El archivo excede el tamaño máximo de ${maxSizeMB}MB.`);
                    input.value = ''; // Resetear el input
                    return;
                }

                // Obtener el elemento img asociado
                const img = input.closest('.custom-image-widget').querySelector('img');

                if (img) {
                    // Crear una URL temporal para la imagen seleccionada
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        img.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            }
        });
    });

    /**
     * Muestra un mensaje de error personalizado debajo del widget.
     * @param {HTMLElement} input - El input de archivo que causó el error.
     * @param {string} mensaje - El mensaje de error a mostrar.
     */
    function mostrarMensajeError(input, mensaje) {
        // Busca si ya existe un mensaje de error
        let mensajeError = input.closest('.custom-image-widget').querySelector('.mensaje-error');
        if (!mensajeError) {
            // Crea un nuevo elemento para el mensaje de error
            mensajeError = document.createElement('div');
            mensajeError.className = 'mensaje-error text-red-500 text-xs mt-2';
            input.closest('.custom-image-widget').appendChild(mensajeError);
        }
        mensajeError.textContent = mensaje;

        // Opcional: Remover el mensaje después de unos segundos
        setTimeout(() => {
            if (mensajeError) {
                mensajeError.remove();
            }
        }, 5000);
    }
});