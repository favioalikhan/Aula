document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const items = carousel.querySelectorAll('.carousel-item');
    const indicators = carousel.querySelectorAll('.indicator');
    let activeIndex = 0;

    function showSlide(index) {
        items.forEach((item, i) => {
            if (i === index) {
                item.classList.add('opacity-100');
                item.classList.remove('opacity-0');
            } else {
                item.classList.remove('opacity-100');
                item.classList.add('opacity-0');
            }
        });

        indicators.forEach((indicator, i) => {
            if (i === index) {
                indicator.classList.add('bg-blue-500'); // Color para el indicador activo
                indicator.classList.remove('bg-white');
            } else {
                indicator.classList.remove('bg-blue-500');
                indicator.classList.add('bg-white');
            }
        });
    }

    function nextSlide() {
        activeIndex = (activeIndex + 1) % items.length;
        showSlide(activeIndex);
    }

    function prevSlide() {
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        showSlide(activeIndex);
    }

    // Configurar indicadores
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            activeIndex = index;
            showSlide(activeIndex);
        });
    });

    // Configurar botones de navegación
    window.nextSlide = nextSlide;
    window.prevSlide = prevSlide;

    // Mostrar la primera diapositiva
    showSlide(0);

    // Cambio automático de diapositivas
    setInterval(nextSlide, 5000);
});