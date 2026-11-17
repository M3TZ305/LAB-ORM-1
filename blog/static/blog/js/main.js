const upload = document.querySelector('input[type="file"][multiple]');
if (upload) upload.addEventListener('change', () => {
    document.getElementById('selected-files').textContent = Array.from(upload.files, file => file.name).join('، ');
    document.getElementById('upload-status').textContent = upload.files.length ? `تم اختيار ${upload.files.length} ملفات` : 'لا توجد ملفات مختارة';
});

const deleteDialog = document.getElementById('delete-dialog');
if (deleteDialog && document.querySelector('[data-delete-open]')) {
    document.querySelector('[data-delete-open]').addEventListener('click', () => {
        deleteDialog.showModal();
        deleteDialog.querySelector('[data-delete-close]').focus();
    });
    deleteDialog.querySelectorAll('[data-delete-close]').forEach(button => button.addEventListener('click', () => deleteDialog.close()));
    deleteDialog.addEventListener('click', event => {
        if (event.target === deleteDialog) {
            const box = deleteDialog.getBoundingClientRect();
            if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) deleteDialog.close();
        }
    });
}


// Keep success feedback visible long enough to read; pause while interacting.
document.querySelectorAll('[data-toast]').forEach(toast => {
    let timer;
    let remaining = 6000;
    let started = 0;
    let dismissed = false;
    const paused = new Set();
    const dismiss = () => {
        if (dismissed) return;
        dismissed = true;
        clearTimeout(timer);
        toast.classList.add('toast-leaving');
        const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.setTimeout(() => toast.remove(), reduced ? 0 : 180);
    };
    const schedule = () => {
        if (dismissed || paused.size || toast.dataset.autohide !== 'true') return;
        started = performance.now();
        timer = window.setTimeout(dismiss, Math.max(remaining, 0));
    };
    const pause = reason => {
        if (!paused.size && started) {
            remaining = Math.max(0, remaining - (performance.now() - started));
            clearTimeout(timer);
            started = 0;
        }
        paused.add(reason);
    };
    const resume = reason => { paused.delete(reason); schedule(); };
    toast.querySelector('[data-toast-close]').addEventListener('click', dismiss);
    toast.addEventListener('mouseenter', () => pause('hover'));
    toast.addEventListener('mouseleave', () => resume('hover'));
    toast.addEventListener('focusin', () => pause('focus'));
    toast.addEventListener('focusout', event => {
        if (!toast.contains(event.relatedTarget)) resume('focus');
    });
    schedule();
});
window.addEventListener('pageshow', event => {
    if (event.persisted) document.querySelectorAll('[data-toast]').forEach(toast => toast.remove());
});
