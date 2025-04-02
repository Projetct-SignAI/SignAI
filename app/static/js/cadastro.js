document.getElementById("cadastro-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
        alert("As senhas não coincidem!");
        return;
    }

    let response = await fetch("/cadastro/info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });

    try {
        let result = await response.json(); // Tenta converter para JSON

        if (response.ok) {
            alert(result.message);
            window.location.href = "/"; // Redireciona para a página de login
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert("Erro ao processar resposta do servidor.");
        console.error("Erro:", error);
    }
});
