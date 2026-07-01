/* ========================================================================
   reveal.js — Animações disparadas pelo scroll
   ------------------------------------------------------------------------
   Duas estratégias, cada uma pela ferramenta certa:

   A) IntersectionObserver (robusto, sem dependência): reveals de entrada,
      contadores numéricos e anéis de progresso. Funciona mesmo se a CDN
      do GSAP cair.

   B) GSAP + ScrollTrigger (progressivo): parallax e o scroll horizontal
      pinado da landing — o "scroll-driven" pesado. Só roda se a lib existir
      e o usuário não pediu prefers-reduced-motion.

   Tudo degrada: sem JS, o conteúdo aparece normal; com reduced-motion, os
   efeitos viram estados finais estáticos.
   ======================================================================== */
window.TF = window.TF || {}; // guard: sobrevive se smooth.js não tiver carregado
(function () {
    'use strict';

    const reduce = TF.reduceMotion;
    const gsap = TF.gsap;
    const ScrollTrigger = TF.ScrollTrigger;

    /* --------------------------------------------------------------
       A1) REVEALS de entrada — [data-reveal]
       Ao entrar na viewport, adicionamos .is-visible (o CSS faz o resto).
       Um único observer para a página toda = barato.
       -------------------------------------------------------------- */
    const revealEls = document.querySelectorAll('[data-reveal]');
    if (revealEls.length) {
        if (reduce || !('IntersectionObserver' in window)) {
            // Sem animação: mostra tudo de imediato.
            revealEls.forEach((el) => el.classList.add('is-visible'));
        } else {
            const io = new IntersectionObserver((entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        obs.unobserve(entry.target); // anima uma vez só
                    }
                });
            }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
            revealEls.forEach((el) => io.observe(el));
        }
    }

    /* --------------------------------------------------------------
       A2) CONTADORES — [data-count="1200"]
       Conta de 0 até o alvo quando entra na tela. rAF puro (sem lib).
       -------------------------------------------------------------- */
    const countEls = document.querySelectorAll('[data-count]');
    const animateCount = (el) => {
        const target = parseFloat(el.getAttribute('data-count')) || 0;
        const dur = 1400;               // ms
        const start = performance.now();
        const easeOut = (t) => 1 - Math.pow(1 - t, 3);
        const step = (now) => {
            const p = Math.min(1, (now - start) / dur);
            el.textContent = Math.round(target * easeOut(p)).toLocaleString('pt-BR');
            if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
    };
    if (countEls.length) {
        if (reduce || !('IntersectionObserver' in window)) {
            countEls.forEach((el) => {
                const t = parseFloat(el.getAttribute('data-count')) || 0;
                el.textContent = t.toLocaleString('pt-BR');
            });
        } else {
            const io = new IntersectionObserver((entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCount(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.6 });
            countEls.forEach((el) => io.observe(el));
        }
    }

    /* --------------------------------------------------------------
       A3) ANÉIS DE PROGRESSO — [data-ring][data-value="42"]
       Anima o stroke-dashoffset do círculo até a % real. A transição do
       traço é feita em CSS; aqui só setamos os valores no momento certo.
       -------------------------------------------------------------- */
    const rings = document.querySelectorAll('[data-ring]');
    const setRing = (ring, animated) => {
        const fill = ring.querySelector('.ring-fill');
        if (!fill) return;
        const r = fill.r.baseVal.value;
        const circ = 2 * Math.PI * r;
        const value = Math.max(0, Math.min(100, parseFloat(ring.getAttribute('data-value')) || 0));
        fill.style.strokeDasharray = circ;
        // Começa "vazio" e depois anima até o valor (offset menor = mais cheio).
        fill.style.strokeDashoffset = circ;
        const paint = () => { fill.style.strokeDashoffset = circ * (1 - value / 100); };
        if (animated) requestAnimationFrame(() => requestAnimationFrame(paint));
        else paint();
    };
    if (rings.length) {
        if (reduce || !('IntersectionObserver' in window)) {
            rings.forEach((ring) => setRing(ring, false));
        } else {
            const io = new IntersectionObserver((entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        setRing(entry.target, true);
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.4 });
            rings.forEach((ring) => io.observe(ring));
        }
    }

    /* ==============================================================
       B) GSAP + ScrollTrigger — só se disponível e sem reduced-motion
       ============================================================== */
    if (!gsap || !ScrollTrigger || reduce) return;

    /* B1) PARALLAX — [data-parallax="0.2"]
       Move o elemento no eixo Y proporcionalmente ao scroll. Valor = força
       (fração da distância percorrida). scrub:true "amarra" ao scroll. */
    gsap.utils.toArray('[data-parallax]').forEach((el) => {
        const strength = parseFloat(el.getAttribute('data-parallax')) || 0.2;
        gsap.to(el, {
            yPercent: -strength * 100,
            ease: 'none',
            scrollTrigger: {
                trigger: el,
                start: 'top bottom',   // começa quando o topo do el toca a base da viewport
                end: 'bottom top',     // termina quando a base sai por cima
                scrub: true            // progresso ligado à barra de scroll
            }
        });
    });

    /* B2) SCROLL HORIZONTAL PINADO — [data-horizontal]
       Fixa a seção na tela e traduz a "trilha" no eixo X conforme o usuário
       rola verticalmente. É o efeito "scrollytelling" clássico.
       No mobile isso degrada pra empilhamento vertical (ver media query CSS +
       a checagem de largura abaixo). */
    const hSection = document.querySelector('[data-horizontal]');
    if (hSection && window.innerWidth > 720) {
        const track = hSection.querySelector('[data-horizontal-track]');
        if (track) {
            // Distância a percorrer = quanto a trilha "passa" da largura da tela.
            const getScrollAmount = () => track.scrollWidth - window.innerWidth;
            gsap.to(track, {
                x: () => -getScrollAmount(),
                ease: 'none',
                scrollTrigger: {
                    trigger: hSection,
                    start: 'top top',
                    // O comprimento do scroll = tamanho da trilha (1px vertical : 1px horizontal)
                    end: () => '+=' + getScrollAmount(),
                    pin: true,           // "prega" a seção enquanto rola
                    scrub: 1,            // leve suavização
                    invalidateOnRefresh: true, // recalcula em resize
                    anticipatePin: 1
                }
            });
        }
    }

    /* B3) Título do hero com leve parallax de opacidade ao sair.
       Deixa a saída do hero mais "cinematográfica". */
    const heroContent = document.querySelector('[data-hero-content]');
    if (heroContent) {
        gsap.to(heroContent, {
            yPercent: 18,
            opacity: 0.2,
            ease: 'none',
            scrollTrigger: {
                trigger: '.lp-hero',
                start: 'top top',
                end: 'bottom top',
                scrub: true
            }
        });
    }

    // Recalcula posições quando as fontes/imagens terminam de carregar.
    window.addEventListener('load', () => ScrollTrigger.refresh());
})();
