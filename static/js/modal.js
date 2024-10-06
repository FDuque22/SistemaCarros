// Função para abrir o modal com a imagem
function openModal(imageUrl) {
    console.log("Modal aberto com a imagem:", imageUrl);
    var modal = document.getElementById("imageModal");
    var modalImage = document.getElementById("modalImage");
    modal.style.display = "flex"; // Alterar para "flex" para centralizar o conteúdo
    modalImage.src = imageUrl;
}

// Função para fechar o modal
function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}

// Fechar o modal ao clicar fora da imagem
window.onclick = function(event) {
    var modal = document.getElementById("imageModal");
    if (event.target === modal) { // Use "===" para comparação estrita
        closeModal();
    }
}
