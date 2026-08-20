window.addEventListener('DOMContentLoaded', () => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);
  const intro = gsap.timeline({defaults: {ease: 'power3.out'}});
  intro.from('body', {opacity: 0, duration: .45})
    .from('.availability', {opacity: 0, y: 14, duration: .45})
    .from('.hero-title > span', {yPercent: 110, opacity: 0, duration: .8}, '-=.15')
    .from('.hero-title strong', {y: 32, opacity: 0, duration: .7}, '-=.4')
    .from('.hero-description', {y: 18, opacity: 0, duration: .55}, '-=.3')
    .from('.hero-actions > *', {y: 15, opacity: 0, stagger: .1, duration: .45}, '-=.2')
    .from('.portrait-shell', {scale: .92, opacity: 0, duration: .85}, '-=.7')
    .from('.orbit', {scale: .86, opacity: 0, stagger: .12, duration: .7}, '-=.5')
    .from('.orbit-item', {scale: .3, opacity: 0, stagger: .06, duration: .4}, '-=.35');

  gsap.utils.toArray('.section-heading, .about-grid h2').forEach(element => {
    gsap.from(element, {scrollTrigger: {trigger: element, start: 'top 86%', once: true}, y: 35, opacity: 0, duration: .8});
  });
  gsap.utils.toArray('.project-card').forEach((element, index) => {
    gsap.from(element, {scrollTrigger: {trigger: element, start: 'top 90%', once: true}, clipPath: 'inset(0 0 100% 0 round 32px)', duration: .9, delay: (index % 2) * .06});
  });
  gsap.from('.timeline-item', {scrollTrigger: {trigger: '.timeline', start: 'top 80%', once: true}, y: 25, opacity: 0, stagger: .09, duration: .6});
  gsap.from('.certificate-card', {scrollTrigger: {trigger: '.certificate-grid', start: 'top 85%', once: true}, scale: .97, opacity: 0, stagger: .08, duration: .55});

  if (window.Lenis) {
    const lenis = new Lenis({duration: 1.05, smoothWheel: true});
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(time => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }
});
