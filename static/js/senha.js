function togglePassword() {
    const passwordField = document.getElementById('password-field'); // Atualizado para referenciar o campo de senha
    const checkbox = document.getElementById('show-password');

    // Alterna o tipo do campo de senha
    if (checkbox.checked) {
        passwordField.type = 'text'; // Altera o tipo do campo para texto
    } else {
        passwordField.type = 'password'; // Altera o tipo de volta para senha
    }
}
