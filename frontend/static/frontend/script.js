document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("particles");

  for (let i = 0; i < 250; i++) {
    let particle = document.createElement("div");
    particle.classList.add("particle");

    // Random position and delay
    particle.style.left = Math.random() * 100 + "vw";
    particle.style.animationDuration = 5 + Math.random() * 5 + "s";
    particle.style.animationDelay = Math.random() * 5 + "s";
    particle.style.width = particle.style.height = Math.random() * 4 + 2 + "px";

    container.appendChild(particle);
  }
});