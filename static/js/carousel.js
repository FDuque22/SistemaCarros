let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-item');

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = 'none';  // Esconde todas as imagens
        slide.classList.remove('active');  // Remove a classe 'active' de todas
    });
    slides[index].style.display = 'block';  // Exibe a imagem atual
    slides[index].classList.add('active');  // Adiciona a classe 'active' à imagem atual
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;  // Vai para o próximo slide, com looping
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;  // Vai para o slide anterior, com looping
    showSlide(currentSlide);
}

// Exibe o primeiro slide ao carregar a página
showSlide(currentSlide);
