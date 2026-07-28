(function () {
    function renderNavbar() {
        // 1. Descobrimos qual é a página atual primeiro
        const path = window.location.pathname.split('/').pop() || 'dashboard.html';
        
        // 2. Criamos uma variável para guardar o botão dinâmico
        let botaoNovoHTML = '';

        // 3. Verificamos a tela e injetamos o botão correto
        if (path === 'clientes.html') {
            botaoNovoHTML = `<button onclick="abrirModalNovoCliente()" style="background-color: #007bff; color: #fff; padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600; margin-right: 15px;">+ Novo Cliente</button>`;
        } else if (path === 'posvendas.html') {
            // Nota: Coloquei 'novo_pos_venda.html' como exemplo. Ajuste se o nome do seu arquivo for diferente!
            botaoNovoHTML = `<button onclick="window.location.href='novo_pos_venda.html'" style="background-color: #d93025; color: #fff; padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600; margin-right: 15px;">+ Novo Pós-Vendas</button>`;
        }

        const existingHeader = document.querySelector('header');
        
        // 4. Montamos o HTML da Navbar incluindo o botão dinâmico
        const headerHTML = `
            <div class="header-logo-wrapper">
                <a href="dashboard.html"><img src="assets/logo.png" alt="Bom Controle NPS" class="header-logo" style="height: 28px !important; width: auto !important; display: block;"></a>
            </div>
            <nav id="nav-menu">
                <a href="dashboard.html" data-page="dashboard.html">Dashboard</a>
                <a href="clientes.html" data-page="clientes.html">Clientes</a>
                <a href="posvendas.html" data-page="posvendas.html">Pós-venda</a>
                <a href="relatorios.html" data-page="relatorios.html">Relatórios</a>
                <a href="avaliacao-completa.html" data-page="avaliacao-completa.html">Avaliações</a>
                <a href="importar.html" data-page="importar.html">Importar</a>
                <a href="auditoria.html" data-page="auditoria.html">Auditoria</a>
            </nav>
            <div style="display: flex; align-items: center;">
                <!-- O botão dinâmico aparece aqui, do lado do botão Sair -->
                ${botaoNovoHTML}
                <button class="btn-logout" onclick="logout()" style="background: transparent; border: 1px solid var(--red); color: var(--red); padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600;">Sair</button>
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

// Função de logout global
if (typeof window.logout !== 'function') {
    window.logout = function () {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = 'index.html';
    };
}