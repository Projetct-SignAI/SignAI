// Carrega header e footer nos elementos-placeholder
document.addEventListener("DOMContentLoaded", () => {
  const inject = (selector, url) =>
    fetch(url)
      .then(res => res.text())
      .then(html => {
        const el = document.querySelector(selector);
        if (el) el.innerHTML = html;
      });

  inject("#header-placeholder", "/static/components/header.html");
  inject("#footer-placeholder", "/static/components/footer.html");
});
