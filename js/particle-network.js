(() => {
  const canvas = document.querySelector(".hero-network");
  if (!canvas) return;

  const context = canvas.getContext("2d");
  if (!context) return;

  const hero = canvas.closest(".hero");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const connectionDistance = 150;
  let particles = [];
  let animationFrame;
  let width = 0;
  let height = 0;

  function resize() {
    const bounds = hero.getBoundingClientRect();
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    width = bounds.width;
    height = bounds.height;
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

    const count = Math.min(120, Math.round((width * height) / 9000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 1.5 + 1,
    }));

    draw();
  }

  function draw() {
    context.clearRect(0, 0, width, height);

    for (let first = 0; first < particles.length; first += 1) {
      const particle = particles[first];

      for (let second = first + 1; second < particles.length; second += 1) {
        const neighbor = particles[second];
        const distance = Math.hypot(particle.x - neighbor.x, particle.y - neighbor.y);
        if (distance >= connectionDistance) continue;

        context.beginPath();
        context.moveTo(particle.x, particle.y);
        context.lineTo(neighbor.x, neighbor.y);
        context.strokeStyle = `rgba(0, 192, 255, ${(1 - distance / connectionDistance) * 0.38})`;
        context.lineWidth = 1;
        context.stroke();
      }

      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fillStyle = "rgba(167, 229, 255, 0.75)";
      context.fill();

      if (!reducedMotion.matches) {
        particle.x += particle.vx;
        particle.y += particle.vy;
        if (particle.x < 0 || particle.x > width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > height) particle.vy *= -1;
      }
    }

    if (!reducedMotion.matches) animationFrame = window.requestAnimationFrame(draw);
  }

  function restart() {
    window.cancelAnimationFrame(animationFrame);
    draw();
  }

  window.addEventListener("resize", resize);
  reducedMotion.addEventListener("change", restart);
  resize();
})();
