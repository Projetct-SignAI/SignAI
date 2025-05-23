/**
 * login.js
 * Autentica o usuário via FastAPI e redireciona para /home.
 * Exibe mensagem de erro em caso de falha.
 */

document
    .getElementById("login-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        try {
            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                window.location.href = "/home";
            } else {
                showError(result.detail || "Usuário ou senha inválidos.");
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            showError("Erro ao processar login.");
        }
    });

function showError(msg) {
    const errorEl = document.getElementById("error-message");
    errorEl.textContent = msg;
    errorEl.style.display = "block";
}
