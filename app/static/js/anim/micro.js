/* ========================================================================
   micro.js — Micro-interações do app
   ------------------------------------------------------------------------
   • Botões magnéticos ([data-magnetic]) — seguem sutilmente o cursor.
   • Concluir tarefa ([data-status-select]) — pulso satisfatório antes do
     POST que recarrega a página (o backend é server-rendered).
   • Deletar tarefa ([data-delete-form]) — animação de saída do card antes
     de enviar o form (mantém o confirm() e a senha exigida pelo backend).
   • Loading nos forms — o botão de submit vira spinner ao enviar.
   Tudo respeita prefers-reduced-motion.
   ======================================================================== */
window.TF = window.TF || {}; // guard: sobrevive se smooth.js não tiver carregado
(function () {
    'use strict';
    const reduce = TF.reduceMotion;

    /* --------------------------------------------------------------
       1) BOTÕES MAGNÉTICOS — [data-magnetic]
       O elemento se desloca uma fração da distância mouse↔centro.
       Só em telas com ponteiro fino (mouse), nunca no touch.
       -------------------------------------------------------------- */
    const finePointer = window.matchMedia('(pointer: fine)').matches;
    if (finePointer && !reduce) {
        document.querySelectorAll('[data-magnetic]').forEach((el) => {
            const strength = parseFloat(el.getAttribute('data-magnetic')) || 0.3;
            el.addEventListener('mousemove', (e) => {
                const rect = el.getBoundingClientRect();
                const mx = e.clientX - (rect.left + rect.width / 2);
                const my = e.clientY - (rect.top + rect.height / 2);
                el.style.transform = `translate(${mx * strength}px, ${my * strength}px)`;
            });
            el.addEventListener('mouseleave', () => {
                el.style.transform = 'translate(0, 0)';
            });
        });
    }

    /* --------------------------------------------------------------
       2) CONCLUIR / MUDAR STATUS — [data-status-select]
       No template, o <select> troca de "pendente"/"concluida" e o form
       precisa dar POST (recarrega). Aqui damos o feedback ANTES de enviar:
       se virou "concluida", um pulso verde no card; senão, envia direto.
       -------------------------------------------------------------- */
    document.querySelectorAll('[data-status-select]').forEach((select) => {
        // Assume o controle: remove o onchange inline (fallback sem-JS) para não
        // dar submit duas vezes. A partir daqui, quem envia é o nosso handler.
        select.removeAttribute('onchange');
        select.addEventListener('change', () => {
            const form = select.form;
            const card = select.closest('.task-card');
            const submit = () => form.submit(); // .submit() ignora onchange/onsubmit
            if (reduce || !card || select.value !== 'concluida') {
                submit();
                return;
            }
            card.classList.add('task-done-pulse');
            // Espera o pulso antes de recarregar (satisfatório, mas curto).
            setTimeout(submit, 420);
        });
    });

    /* --------------------------------------------------------------
       3) DELETAR — [data-delete-form]
       O confirm() inline roda primeiro (mantido no template). Se confirmado,
       animamos a saída do card e só então enviamos o form de verdade.
       -------------------------------------------------------------- */
    document.querySelectorAll('[data-delete-form]').forEach((form) => {
        form.addEventListener('submit', (e) => {
            if (reduce) return; // deixa enviar normal
            const card = form.closest('.task-card');
            if (!card || card.classList.contains('task-exit')) return; // evita loop
            e.preventDefault();
            card.classList.add('task-exit');
            setTimeout(() => form.submit(), 340); // casa com a transição do CSS
        });
    });

    /* --------------------------------------------------------------
       4) LOADING nos forms — botão de submit vira spinner
       Feedback imediato enquanto o servidor processa/redireciona.
       Não aplicamos em forms de delete (o card já anima saindo).
       -------------------------------------------------------------- */
    document.querySelectorAll('form').forEach((form) => {
        if (form.hasAttribute('data-delete-form')) return;
        form.addEventListener('submit', () => {
            const btn = form.querySelector('button[type="submit"], button:not([type])');
            if (btn && !reduce) btn.classList.add('is-loading');
        });
    });
})();
