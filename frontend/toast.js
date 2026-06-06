function toast(mensagem, tipo = 'sucesso') {
    const cores = {
        sucesso: '#00cc66',
        erro: '#cc0000',
        aviso: '#f59e0b',
        info: '#38bdf8'
    };

    const t = document.createElement('div');
    t.textContent = mensagem;
    t.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: #1e1e1e;
        color: #f1f1f1;
        padding: 14px 20px;
        border-radius: 10px;
        border-left: 4px solid ${cores[tipo]};
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        z-index: 9999;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        max-width: 320px;
    `;

    document.body.appendChild(t);

    setTimeout(() => {
        t.style.opacity = '1';
        t.style.transform = 'translateY(0)';
    }, 10);

    setTimeout(() => {
        t.style.opacity = '0';
        t.style.transform = 'translateY(10px)';
        setTimeout(() => t.remove(), 300);
    }, 3000);
}