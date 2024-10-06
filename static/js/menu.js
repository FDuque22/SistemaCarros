document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle'); // O botão que ativa o menu
    const navbar = document.querySelector('.navbar'); // O contêiner do menu

    menuToggle.addEventListener('click', function() {
        navbar.classList.toggle('active'); // Alterna a classe 'active' para mostrar/esconder o menu
    });
});
