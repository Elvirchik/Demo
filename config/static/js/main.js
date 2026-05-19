document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('#burger');
  const nav = document.querySelector('#nav');
  if (burger && nav) {
    burger.addEventListener('click', () => nav.classList.toggle('open'));
  }

  document.querySelectorAll('[data-slider]').forEach(slider => {
    const slides = slider.querySelectorAll('.slide');
    const prev = slider.querySelector('[data-prev]');
    const next = slider.querySelector('[data-next]');
    let index = 0;

    function showSlide(newIndex) {
      slides[index].classList.remove('active');
      index = (newIndex + slides.length) % slides.length;
      slides[index].classList.add('active');
    }

    next.addEventListener('click', () => showSlide(index + 1));
    prev.addEventListener('click', () => showSlide(index - 1));
    setInterval(() => showSlide(index + 1), 3000);
  });
});
