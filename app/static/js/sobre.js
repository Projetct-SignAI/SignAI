document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".timeline-track");
  const prev = document.querySelector(".timeline-nav.prev");
  const next = document.querySelector(".timeline-nav.next");

  if (!track || !prev || !next) return;

  const step = 300; // quanto irá rolar por clique

  prev.addEventListener("click", () => {
    track.scrollBy({ left: -step, behavior: "smooth" });
  });

  next.addEventListener("click", () => {
    track.scrollBy({ left: step, behavior: "smooth" });
  });
});
