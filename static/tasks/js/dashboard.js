/**
 * Implements a two-tab dashboard and lazy-fetching of REST endpoints
 */
export function TabbedDashBoard(idToCheck) {
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
        console.log('[setActiveTab] Checking if id made it: ', idToCheck)
        tabs.forEach(tab => {
            const name = tab.dataset.tab;
            const pane = document.getElementById('tab-' + name);
            if (name === tabName) {
                tab.classList.add('active');
                tab.setAttribute('aria-selected','true');
                pane.classList.add('active');
            } else {
                tab.classList.remove('active');
                tab.setAttribute('aria-selected','false');
                pane.classList.remove('active');
            }
        });
    }

    async function fetchTab(tabName) {
        console.log('[fetchTab] Checking if id made it: ', idToCheck)
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
        console.log('[renderData] Checking if id made it: ', idToCheck)
        const container = containers[tabName];
        if (Array.isArray(data)) {
            const ul = document.createElement('ul');
            ul.className = 'list-group';
            data.forEach(item => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                let desc = item.description || JSON.stringify(item);
                let meta = item.status ? '<div class="text-muted small">' + escapeHtml(item.status) + '</div>' : '';
                let more = ''
                let details = ''
                if (tabName == 'private') {
                        more = '<a class="btn position-absolute top-0 end-0 m-3" data-bs-toggle="collapse" href="#collapseExample-' + escapeHtml(item.id) + '" role="button" aria-expanded="false" aria-controls="collapseExample-' + escapeHtml(item.id) + '"><i class="bi bi-info-circle"></i></a>'
                        details = '<div class="collapse" id="collapseExample-' + escapeHtml(item.id) + '"><div class="card card-body">' + escapeHtml(item.details) + '</div></div>'
                }
                li.innerHTML = '<div class="position-relative"><a class="link" href="/tasks/details/' + escapeHtml(item.id) + '">' + escapeHtml(String(desc)) + '</a>' + meta + more + details + '</div>';
                ul.appendChild(li);
            });
            container.innerHTML = '';
            container.appendChild(ul);
        } else {
            container.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        }
    }

    function escapeHtml(str) {
        console.log('[escapeHtml] Checking if id made it: ', idToCheck)
        return String(str).replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
    }

    /**
     * This sets the event handler for tables loading data
     */
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            console.log('Checking if id made it (inside | tabs.forEach -> add eventListener): ', idToCheck)
            let info = tab.dataset.tab;
            setActiveTab(info);
            fetchTab(info);
        });

        if (tab.id == 'tab-private-btn') {
            console.log('Checking if id made it (inside if of triggering private tab): ', idToCheck)
            // trigger 'private' tab by default
            tab.click()
        }
    });

    console.log('Checking inside constructore, can I call id directly?', idToCheck)

}

