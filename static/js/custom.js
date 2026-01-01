/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 * Implements a two-tab dashboard and lazy-fetching of REST endpoints
 */

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('#tasksTab .nav-link');
    const containers = {
        private: document.getElementById('privateContainer'),
        workspaces: document.getElementById('workspacesContainer'),
    };
    const spinners = {
        private: document.getElementById('privateSpinner'),
        workspaces: document.getElementById('workspacesSpinner'),
    };
    const endpoints = {
        private: '/rest/tasks/private',
        workspaces: '/rest/tasks/workspaces',
    };
    const fetched = { private: false, workspaces: false };

    function setActiveTab(tabName) {
        tabs.forEach(t => {
            const name = t.dataset.tab;
            const pane = document.getElementById('tab-' + name);
            if (name === tabName) {
                t.classList.add('active');
                t.setAttribute('aria-selected','true');
                pane.classList.add('active');
            } else {
                t.classList.remove('active');
                t.setAttribute('aria-selected','false');
                pane.classList.remove('active');
            }
        });
    }

    async function fetchTab(tabName) {
        if (fetched[tabName]) return;
        fetched[tabName] = true;
        const spinner = spinners[tabName];
        const container = containers[tabName];
        spinner.classList.remove('d-none');
        try {
            const res = await fetch(endpoints[tabName], { credentials: 'same-origin' });
            if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
            const contentType = res.headers.get('content-type') || '';
            if (contentType.includes('application/json')) {
                const data = await res.json();
                console.log('This is data var: 1', data.results)
                renderData(tabName, data.results);
            } else {
                const text = await res.text();
                container.innerHTML = '<pre>' + escapeHtml(text) + '</pre>';
            }
        } catch (err) {
            container.innerHTML = '<div class="alert alert-danger">Error loading: ' + escapeHtml(err.message) + '</div>';
        } finally {
            spinner.classList.add('d-none');
        }
    }

    function renderData(tabName, data) {
        const container = containers[tabName];
        if (Array.isArray(data)) {
            const ul = document.createElement('ul');
            ul.className = 'list-group';
            data.forEach(item => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                const desc = item.description || JSON.stringify(item);
                const meta = item.status ? '<div class="text-muted small">' + escapeHtml(item.status) + '</div>' : '';
                var more = ''
                var details = ''
                console.log('What is the tabName currently?', tabName)
                if (tabName == 'private') {
                        more = '<a class="btn position-absolute top-0 end-0 m-3" data-bs-toggle="collapse" href="#collapseExample-' + escapeHtml(item.id) + '" role="button" aria-expanded="false" aria-controls="collapseExample-' + escapeHtml(item.id) + '"><i class="bi bi-info-circle"></i></a>'
                        details = '<div class="collapse" id="collapseExample-' + escapeHtml(item.id) + '"><div class="card card-body">' + escapeHtml(item.details) + '</div></div>'
                }
                li.innerHTML = '<div class="position-relative"><div>' + escapeHtml(String(desc)) + '</div>' + meta + more + details + '</div>';
                ul.appendChild(li);
            });
            container.innerHTML = '';
            container.appendChild(ul);
        } else {
            container.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        }
    }

    function escapeHtml(str) {
        return String(str).replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
    }

    tabs.forEach(t => {
        t.addEventListener('click', () => {
            const tab = t.dataset.tab;
            setActiveTab(tab);
            fetchTab(tab);
        });
    });

    // Default open: private tab
    setActiveTab('private');
    fetchTab('private');
});
