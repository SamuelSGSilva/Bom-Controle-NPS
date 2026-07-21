(function () {
    function renderNavbar() {
        const existingHeader = document.querySelector('header');
        const headerHTML = `
            <div class="header-logo-wrapper">
                <a href="dashboard.html"><img src="assets/logo.png" alt="Bom Controle NPS" class="header-logo"></a>
            </div>
            <nav id="nav-menu">
                <a href="dashboard.html" data-page="dashboard.html">Dashboard</a>
                <a href="clientes.html" data-page="clientes.html">Clientes</a>
                <a href="novo-cliente.html" data-page="novo-cliente.html">Novo Cliente</a>
                <a href="posvendas.html" data-page="posvendas.html">Pós-venda</a>
                <a href="novo-posvendas.html" data-page="novo-posvendas.html">Novo Pós-Vendas</a>
                <a href="relatorios.html" data-page="relatorios.html">Relatórios</a>
                <a href="avaliacao-completa.html" data-page="avaliacao-completa.html">Avaliações</a>
                <a href="importar.html" data-page="importar.html">Importar</a>
                <a href="auditoria.html" data-page="auditoria.html">Auditoria</a>
            </nav>
            <div style="display: flex; align-items: center; gap: 12px;">
                <button class="btn-logout" onclick="logout()">Sair</button>
                <button class="mobile-toggle" onclick="toggleMenuMobile()" aria-label="Menu">☰</button>
            </div>
        `;

        if (existingHeader) {
            existingHeader.innerHTML = headerHTML;
        } else {
            const header = document.createElement('header');
            header.innerHTML = headerHTML;
            document.body.prepend(header);
        }

        // Destacar página ativa
        const path = window.location.pathname.split('/').pop() || 'dashboard.html';
        const navLinks = document.querySelectorAll('nav a');
        navLinks.forEach(link => {
            const page = link.getAttribute('data-page');
            if (page === path || (path === '' && page === 'dashboard.html')) {
                link.classList.add('ativo');
            } else {
                link.classList.remove('ativo');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderNavbar);
    } else {
        renderNavbar();
    }
})();

function toggleMenuMobile() {
    const nav = document.getElementById('nav-menu');
    if (nav) {
        nav.classList.toggle('aberto');
    }
}

if (typeof window.logout !== 'function') {
    window.logout = function () {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = 'index.html';
    };
}
