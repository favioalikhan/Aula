document.addEventListener("DOMContentLoaded", function() {
    // Esperar 2 segundos antes de ocultar el loader
    const loader = document.getElementById("loader");
    setTimeout(function() {
        loader.classList.add("hidden");
    }, 2000); // 2000 ms = 2 segundos
});