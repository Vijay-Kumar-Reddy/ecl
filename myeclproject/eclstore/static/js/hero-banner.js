$(function () {

  const slider = $(".hero-slider");

  if (slider.length === 0) return;

  const slides = slider.find(".hero-slide");
  const dots = slider.find(".hero-dot");

  let current = 0;
  let animating = false;

  function showSlide(index, direction = 1) {
    if (animating || index === current) return;
    animating = true;

    const currentSlide = slides.eq(current);
    const nextSlide = slides.eq(index);

    const offset = direction * 100;

    gsap.set(nextSlide, {
      xPercent: offset,
      display: "block",
      opacity: 1,
      zIndex: 2,
    });

    gsap.timeline({
      onComplete: () => {
        currentSlide.removeClass("is-active").css({ zIndex: 1 });
        nextSlide.addClass("is-active").css({ zIndex: 2 });
        gsap.set(currentSlide, { xPercent: 0, display: "" });
        dots.removeClass("is-active").eq(index).addClass("is-active");
        current = index;
        animating = false;
      },
    })
    .to(currentSlide, { xPercent: -offset, duration: 1, ease: "power2.inOut" }, 0)
    .to(nextSlide, { xPercent: 0, duration: 1, ease: "power2.inOut" }, 0);
  }

  function nextSlide() {
    const nextIndex = (current + 1) % slides.length;
    showSlide(nextIndex, 1);
  }

  function prevSlide() {
    const prevIndex = (current - 1 + slides.length) % slides.length;
    showSlide(prevIndex, -1);
  }

  slider.find(".hero-next").on("click", () => nextSlide());
  slider.find(".hero-prev").on("click", () => prevSlide());

  dots.on("click", function () {
    const index = $(this).index();
    const direction = index > current ? 1 : -1;
    showSlide(index, direction);
  });

  slides.eq(current).addClass("is-active").css({ display: "block", zIndex: 2 });

});
