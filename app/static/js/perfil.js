(async () => {
  const msgEl   = document.getElementById("msg");
  const nameEl  = document.getElementById("name");
  const emailEl = document.getElementById("email");
  const passEl  = document.getElementById("password");

  const token = localStorage.getItem("signai_token");

  // 1️⃣ Preenche dados atuais
  try {
    const r = await fetch("/user-info", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!r.ok) throw new Error("Falha ao obter dados");
    const data = await r.json();
    nameEl.value = data.name || "";
    emailEl.value = data.email || "";
  } catch (e) {
    msgEl.textContent = "Não foi possível carregar informações.";
    msgEl.className = "msg error";
    msgEl.style.display = "block";
  }

  // 2️⃣ Envia alterações
  document.getElementById("profile-form").addEventListener("submit", async (evt) => {
    evt.preventDefault();
    msgEl.style.display = "none";

    const payload = {
      name: nameEl.value.trim(),
      email: emailEl.value.trim(),
      password: passEl.value.trim() || undefined
    };

    try {
      const res = await fetch("/update-profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.ok) {
        if (data.access_token) {
          localStorage.setItem("signai_token", data.access_token);
        }
        msgEl.textContent = "Dados atualizados com sucesso!";
        msgEl.className = "msg success";
        passEl.value = "";
      } else {
        msgEl.textContent = data.detail || "Erro ao salvar";
        msgEl.className = "msg error";
      }
    } catch (err) {
      msgEl.textContent = "Falha ao salvar alterações.";
      msgEl.className = "msg error";
    }

    msgEl.style.display = "block";
  });
})();
