function openModal(imageUrl) {
    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");
    modal.style.display = "flex"; 
    modalImage.src = imageUrl;
}

function closeModal() {
    const modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
