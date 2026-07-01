/* ========================================================================
   transitions.js — Transição de página (wipe via overlay)
   ------------------------------------------------------------------------
   O backend é multi-página (cada navegação recarrega). Para dar a sensação
   de SPA, usamos um overlay que:
     • COBRE a tela ao clicar num link interno (antes de navegar);
     • REVELA a próxima página (o overlay começa cobrindo e sai).

   Sem flash: um script inline no <head> (ver base.html) coloca a classe
   `tf-incoming` no <html> ANTES da primeira pintura quando viemos de uma
   transição — assim o overlay já está cobrindo quando a página aparece.

   Regras de segurança:
     • Só intercepta links GET internos, mesma origem, sem target/modificador.
     • Forms (POST: login, criar, deletar…) seguem o fluxo normal do navegador.
     • prefers-reduced-motion: navegação instantânea, sem overlay.
   ======================================================================== */
window.TF = window.TF || {}; // guard: sobrevive se smooth.js não tiver carregado
(function () {
    'use strict';
    const reduce = TF.reduceMotion;
    const gsap = TF.gsap;
    const overlay = document.querySelector('.tf-overlay');
    const html = document.documentElement;
    const FLAG = 'tf-transition';

    // Sem overlay ou reduced-motion: só limpa qualquer estado e sai.
    if (!overlay || reduce) {
        sessionStorage.removeItem(FLAG);
        html.classList.remove('tf-incoming');
        if (overlay) overlay.style.transform = 'scaleY(0)';
        return;
    }

    /* ---------- REVELAR a página que acabou de entrar ---------- */
    if (html.classList.contains('tf-incoming')) {
        sessionStorage.removeItem(FLAG);
        const reveal = () => {
            html.classList.remove('tf-incoming');
            if (gsap) {
                // Overlay some subindo (origin top): scaleY 1 -> 0.
                gsap.set(overlay, { transformOrigin: 'top' });
                gsap.to(overlay, {
                    scaleY: 0,
                    duration: 0.6,
                    ease: 'power4.inOut',
                    onComplete: () => overlay.classList.remove('is-covering')
                });
            } else {
                overlay.style.transition = 'transform 0.5s cubic-bezier(0.16,1,0.3,1)';
                overlay.style.transformOrigin = 'top';
                overlay.style.transform = 'scaleY(0)';
            }
        };
        // Pequeno atraso pra garantir que a nova página pintou.
        requestAnimationFrame(() => requestAnimationFrame(reveal));
    }

    /* ---------- COBRIR a tela e então navegar ---------- */
    const cover = (href) => {
        sessionStorage.setItem(FLAG, '1'); // sinaliza pro <head> da próxima página
        overlay.classList.add('is-covering');
        const go = () => { window.location.href = href; };
        if (gsap) {
            gsap.set(overlay, { transformOrigin: 'bottom' });
            gsap.to(overlay, {
                scaleY: 1,
                duration: 0.55,
                ease: 'power4.inOut',
                onComplete: go
            });
        } else {
            overlay.style.transition = 'transform 0.45s cubic-bezier(0.16,1,0.3,1)';
            overlay.style.transformOrigin = 'bottom';
            overlay.style.transform = 'scaleY(1)';
            setTimeout(go, 450);
        }
    };

    // É um link que devemos interceptar?
    const isInternalNav = (a) => {
        if (!a || !a.href) return false;
        if (a.target && a.target !== '_self') return false;
        if (a.hasAttribute('download')) return false;
        if (a.hasAttribute('data-no-transition')) return false;
        const url = new URL(a.href, window.location.href);
        if (url.origin !== window.location.origin) return false;      // externo
        if (url.pathname === window.location.pathname && url.hash) return false; // âncora interna
        if (a.getAttribute('href')?.startsWith('#')) return false;
        return true;
    };

    document.addEventListener('click', (e) => {
        // Ignora cliques com modificador (abrir em nova aba etc.)
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
        const a = e.target.closest('a');
        if (!isInternalNav(a)) return;
        e.preventDefault();
        cover(a.href);
    });

    // Se o usuário volta pelo histórico (bfcache), garante overlay limpo.
    window.addEventListener('pageshow', (ev) => {
        if (ev.persisted) {
            html.classList.remove('tf-incoming');
            overlay.classList.remove('is-covering');
            if (gsap) gsap.set(overlay, { scaleY: 0 });
            else overlay.style.transform = 'scaleY(0)';
        }
    });
})();
