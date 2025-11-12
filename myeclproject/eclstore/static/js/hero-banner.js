$(function () {
  const slider = $(".hero-slider");
  const slides = slider.find(".hero-slide");
  const dots = slider.find(".hero-dot");
  const duration = parseInt(slider.data("duration"), 10) || 5000;

  let current = 0;
  let timer;
  let animating = false;

  function showSlide(index, direction = 1, auto = false) {
    if (animating || index === current) return;
    animating = true;

    const currentSlide = slides.eq(current);
    const nextSlide = slides.eq(index);

    // Determine direction: 1 for next, -1 for prev
    const offset = direction * 100;

    gsap.set(nextSlide, {
      xPercent: offset,
      display: "block",
      opacity: 1,
      zIndex: 2,
    });

    const tl = gsap.timeline({
      onComplete: () => {
        currentSlide.removeClass("is-active").css({ zIndex: 1 });
        nextSlide.addClass("is-active").css({ zIndex: 2 });
        gsap.set(currentSlide, { xPercent: 0, display: "" });
        dots.removeClass("is-active").eq(index).addClass("is-active");
        current = index;
        animating = false;
        if (auto) restartTimer();
      },
    });

    tl.to(currentSlide, { xPercent: -offset, duration: 1, ease: "power2.inOut" }, 0)
      .to(nextSlide, { xPercent: 0, duration: 1, ease: "power2.inOut" }, 0);
  }

  function nextSlide(auto = false) {
    const nextIndex = (current + 1) % slides.length;
    showSlide(nextIndex, 1, auto);
  }

  function prevSlide() {
    const prevIndex = (current - 1 + slides.length) % slides.length;
    showSlide(prevIndex, -1, true);
  }

  function startTimer() {
    timer = setInterval(() => nextSlide(true), duration);
  }

  function restartTimer() {
    clearInterval(timer);
    startTimer();
  }

  // Event bindings
  slider.find(".hero-next").on("click", () => {
    nextSlide();
    restartTimer();
  });

  slider.find(".hero-prev").on("click", () => {
    prevSlide();
    restartTimer();
  });

  dots.on("click", function () {
    const index = $(this).index();
    const direction = index > current ? 1 : -1;
    showSlide(index, direction, true);
    restartTimer();
  });

  // Init
  slides.eq(current).addClass("is-active").css({ display: "block", zIndex: 2 });
  startTimer();
});
