document.addEventListener("DOMContentLoaded", function() {
    // Esperar 2 segundos antes de ocultar el loader
    const loader = document.getElementById("loader");
    setTimeout(function() {
        loader.classList.add("hidden");
    }, 1200); // 2000 ms = 2 segundos
});