/* =========================================================
   Espaço Terapêutico Sonho e Luz — interações
   ========================================================= */
(function () {
  'use strict';

  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- ano no rodapé ---------- */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();

  /* ---------- nav: estado fixo ao rolar ---------- */
  var nav = document.getElementById('nav');
  function estadoNav() {
    if (!nav) return;
    nav.classList.toggle('is-fixa', window.scrollY > 40);
  }
  estadoNav();
  window.addEventListener('scroll', estadoNav, { passive: true });

  /* ---------- menu mobile ---------- */
  var hamb = document.getElementById('hamb');
  var menu = document.getElementById('menu');

  function fecharMenu() {
    if (!hamb || !menu) return;
    menu.classList.remove('is-aberto');
    hamb.setAttribute('aria-expanded', 'false');
    hamb.setAttribute('aria-label', 'Abrir menu');
  }

  if (hamb && menu) {
    hamb.addEventListener('click', function () {
      var aberto = menu.classList.toggle('is-aberto');
      hamb.setAttribute('aria-expanded', String(aberto));
      hamb.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) fecharMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') fecharMenu();
    });

    document.addEventListener('click', function (e) {
      if (!menu.classList.contains('is-aberto')) return;
      if (e.target.closest('#menu') || e.target.closest('#hamb')) return;
      fecharMenu();
    });
  }

  /* ---------- acordeão do FAQ ---------- */
  var botoes = document.querySelectorAll('.acordeao__botao');
  Array.prototype.forEach.call(botoes, function (botao) {
    botao.addEventListener('click', function () {
      var item = botao.closest('.acordeao__item');
      var aberto = botao.getAttribute('aria-expanded') === 'true';

      // fecha os demais (comportamento de acordeão)
      Array.prototype.forEach.call(botoes, function (outro) {
        if (outro === botao) return;
        outro.setAttribute('aria-expanded', 'false');
        var o = outro.closest('.acordeao__item');
        if (o) o.classList.remove('is-aberto');
      });

      botao.setAttribute('aria-expanded', String(!aberto));
      if (item) item.classList.toggle('is-aberto', !aberto);
    });
  });

  /* ---------- revelação suave ao entrar na viewport ---------- */
  var alvos = document.querySelectorAll(
    '.selo, .cap__cabecalho, .cap01__texto, .cap01__midia, .ficha, ' +
    '.trilha__passo, .cartao, .tambem, .mara__retrato, .mara__texto, ' +
    '.depo__card, .mosaico__item, .acordeao__item, .faq__intro, ' +
    '.contato__info, .contato__mapa'
  );

  if (reduzido || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(alvos, function (el) {
      el.classList.add('is-visivel');
    });
    return;
  }

  Array.prototype.forEach.call(alvos, function (el, i) {
    el.classList.add('reveal');
    el.style.transitionDelay = (i % 4) * 70 + 'ms';
  });

  var observador = new IntersectionObserver(
    function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add('is-visivel');
        observador.unobserve(entrada.target);
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
  );

  Array.prototype.forEach.call(alvos, function (el) {
    observador.observe(el);
  });
})();
