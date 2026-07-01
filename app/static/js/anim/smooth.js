/* ========================================================================
   smooth.js — Fundação da camada de animação
   ------------------------------------------------------------------------
   Responsável por:
     • Detectar prefers-reduced-motion e a presença das libs (Lenis/GSAP).
     • Ligar o smooth scroll (Lenis) e SINCRONIZAR com o ScrollTrigger do GSAP
       — sem isso, o scroll suave e as animações de scroll brigam (jitter).
     • Expor tudo em window.TF para os outros módulos usarem.
   Carrega ANTES de reveal/micro/transitions (ordem garantida por `defer`).
   ======================================================================== */
window.TF = window.TF || {};

(function () {
    'use strict';

    // 1) Usuário pediu menos movimento? Então nada de scroll-jacking/parallax.
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 2) As libs vieram da CDN? Se não, degradamos com elegância.
    const hasGSAP  = typeof window.gsap !== 'undefined';
    const hasST    = hasGSAP && typeof window.ScrollTrigger !== 'undefined';
    const hasLenis = typeof window.Lenis !== 'undefined';

    TF.reduceMotion = reduceMotion;
    TF.gsap = hasGSAP ? window.gsap : null;
    TF.ScrollTrigger = null;

    if (hasST) {
        window.gsap.registerPlugin(window.ScrollTrigger);
        TF.ScrollTrigger = window.ScrollTrigger;
    }

    // 3) Marca o <html> pra que o CSS possa esconder elementos [data-reveal]
    //    APENAS quando sabemos que vamos animá-los (evita sumiço permanente).
    if (!reduceMotion) {
        document.documentElement.classList.add('js-anim');
    }

    // 4) Smooth scroll com Lenis (só se houver lib e o usuário permitir).
    if (hasLenis && !reduceMotion) {
        const lenis = new window.Lenis({
            duration: 1.1,                                   // "peso" do scroll
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // easeOutExpo
            smoothWheel: true,
            wheelMultiplier: 1,
            touchMultiplier: 1.6
        });
        TF.lenis = lenis;

        if (hasGSAP) {
            // Ponte Lenis <-> ScrollTrigger: a cada scroll do Lenis, mandamos o
            // ScrollTrigger recalcular; e rodamos o rAF do Lenis dentro do
            // ticker do GSAP pra ambos usarem o MESMO relógio (sincronizados).
            lenis.on('scroll', () => {
                if (TF.ScrollTrigger) TF.ScrollTrigger.update();
            });
            window.gsap.ticker.add((time) => lenis.raf(time * 1000)); // s -> ms
            window.gsap.ticker.lagSmoothing(0);
        } else {
            // Sem GSAP: tocamos o Lenis no rAF do próprio browser.
            const raf = (time) => { lenis.raf(time); requestAnimationFrame(raf); };
            requestAnimationFrame(raf);
        }
    }

    // 5) Helper: rolar suavemente até um alvo (usado pelo CTA/scroll cue).
    TF.scrollTo = function (target) {
        if (TF.lenis) TF.lenis.scrollTo(target, { offset: 0 });
        else {
            const el = typeof target === 'string' ? document.querySelector(target) : target;
            if (el) el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
        }
    };

    TF.ready = true;
})();
