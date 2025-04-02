document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    console.log("Tentando login com:", { email, password });

    let formData = new URLSearchParams();
    formData.append("username", email);  // 🔹 OAuth2PasswordRequestForm usa "username" (não "email")!
    formData.append("password", password);

    try {
        let response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        let result = await response.json();

        if (response.ok) {
            console.log("Login bem-sucedido:", result);
            alert("Login realizado com sucesso!");
            window.location.href = "/home"; 
        } else {
            console.error("Erro no login:", result);
            alert(result.detail);
        }
    } catch (error) {
        console.error("Erro ao tentar login:", error);
        alert("Erro ao processar login.");
    }
});
