function showTab(tabName, buttonId) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.add('hidden'));
    document.getElementById(tabName).classList.remove('hidden');

    const buttons = document.querySelectorAll('#tabs button');
    buttons.forEach(button => button.classList.remove('bg-blue-500', 'text-white'));
    document.getElementById(buttonId).classList.add('bg-blue-500', 'text-white');
}

// Mostrar la pestaña de emprendedores por defecto y pintar el botón
showTab('emprendedores', 'btn-emprendedores');

// Mantener el botón pintado al hacer clic fuera del grid o en la página
document.addEventListener('click', function(event) {
    const buttons = document.querySelectorAll('#tabs button');
    buttons.forEach(button => {
        if (button.classList.contains('bg-blue-500')) {
            button.classList.add('bg-blue-500', 'text-white');
        }
    });
});