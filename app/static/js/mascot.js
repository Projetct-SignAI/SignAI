document.addEventListener('DOMContentLoaded', () => {
  /* carrega o componente HTML e depois ativa listeners */
  fetch('/static/components/mascot.html')
    .then(r => r.text())
    .then(html => {
      document.body.insertAdjacentHTML('beforeend', html);

      const openBtn  = document.getElementById('open-mascot');
      const closeBtn = document.getElementById('close-mascot');
      const overlay  = document.getElementById('mascot-overlay');
      const popup    = document.getElementById('mascot-popup');

      const open  = () => { overlay.classList.add('active'); popup.classList.add('active'); };
      const close = () => { overlay.classList.remove('active'); popup.classList.remove('active'); };

      openBtn .addEventListener('click', open );
      closeBtn.addEventListener('click', close);
      overlay .addEventListener('click', close);
    })
    .catch(err => console.error('Erro ao carregar o mascote:', err));
});
