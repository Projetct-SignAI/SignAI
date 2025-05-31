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
                window.location.href = "/";
            } else {
                let errorMessage = "Erro ao cadastrar.";

                if (Array.isArray(result.detail)) {
                    errorMessage = result.detail.map(err => err.msg.replace(/^Value error,?\s*/i, '')).join(" | ");
                } else if (typeof result.detail === "string") {
                    errorMessage = result.detail;
                } else if (result.message) {
                    errorMessage = result.message;
                }


                showError(errorMessage);

            }

            
        } catch (error) {
            console.error("Erro:", error);
            showError("Erro ao processar solicitação.");
        }
    });
function showError(msg) {
    const errorEl = document.getElementById("error-message");
    errorEl.textContent = msg.trim();
    errorEl.style.display = "block";
}

