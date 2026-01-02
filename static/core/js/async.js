
/**
 * This class will be used generically to handle all GET calls to RestAPIs
 */
export function Fetcher() {
    const spinners = {};

    /**
     * helps form a proper request definition object
     */
    function defineRequest(url, headers = { 'Content-Type': 'application/json' }) {
        return new Request(url, {
            method: 'GET',
            headers: headers,
            // ... other options
        });
    }

    /**
     * Get or Set spinner element.
     */
    function spinnerElement(id, container = null) {
        if (container !== null && container instanceof HTMLElement) {
            container.innerHTML = '<div class="spinner-border text-primary" role="status" id=' + id +'><span class="visually-hidden">Loading...</span></div>';
        }

        if (id in spinners) {
            return spinners[id];
        }

        spinner = document.getElementById(id)

        if (spinner instanceof HTMLElement) {
            spinners[spinner.id] = spinner;
            return spinner;
        }

        return null;
    }

    /**
     * Performs the actual HTTP request.
     * Handles container and spinner states as well (partially).
     * @param {*} request - Request object
     * @param {*} container - DOM element
     * @param {*} spinner - DOM element
     */
    async function fetchResource(request, container, spinner) {
        try {
            const response = await fetch(request);
            
            if (!response.ok) {
                throw new Error(response.status + ' ' + response.statusText);
            }

            const contentType = response.headers.get('content-type') || '';
            
            if (contentType.includes('application/json')) {
                const data = await response.json();
                renderData(container, data.results);
            } else {
                const text = await response.text();
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
}