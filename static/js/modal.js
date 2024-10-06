<script>
    function openModal(imageUrl) {
        const modal = document.getElementById("imageModal");
        const modalImage = document.getElementById("modalImage");
        modal.style.display = "flex"; // Muda para "flex" para centralizar o conteúdo
        modalImage.src = imageUrl;
    }

    function closeModal() {
        const modal = document.getElementById("imageModal");
        modal.style.display = "none";
    }
    
    // Adicionando o evento de clique às imagens da galeria
    document.addEventListener("DOMContentLoaded", function() {
        const carouselItems = document.querySelectorAll(".carousel-item");
        carouselItems.forEach(item => {
            item.addEventListener("click", function() {
                const imageUrl = this.src; // Obtém a URL da imagem clicada
                openModal(imageUrl); // Abre o modal com a imagem clicada
            });
        });
    });
</script>
