/**
 * cadastro.js
 * Envia dados de cadastro para a API, valida senhas e redireciona para a página de login.
 */

document
    .getElementById("cadastro-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (password !== confirmPassword) {
            showError("As senhas não coincidem!");
            return;
        }

        try {
            const response = await fetch("/cadastro/info", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password })
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message || "Cadastro realizado com sucesso!");
                window.location.href = "/"; // volta para login
            } else {
                showError(result.message || "Erro ao cadastrar.");
            }
        } catch (error) {
            console.error("Erro:", error);
            showError("Erro ao processar solicitação.");
        }
    });

/**
 * Exibe mensagem de erro ao usuário
 */
function showError(msg) {
    const errorEl = document.getElementById("error-message");
    errorEl.textContent = msg;
    errorEl.style.display = "block";
}
