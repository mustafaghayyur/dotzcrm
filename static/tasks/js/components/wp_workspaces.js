import $A from "../helper.js";


export default (data, containerId) => {
    console.log('I made it here 1');
    let container = $A.app.containerElement(containerId);
    if ($A.generic.checkVariableType(container) !== 'domelement') {
        throw Error('UI Error: Dom element for makeNewPane() not valid.');
    }
    let tabs = container.querySelector('.nav-tabs');
    let panes = container.querySelector('.tab-content');
    let tabTemplate = container.querySelector('.nav-tabs .nav-item');
    let paneTemplate = container.querySelector('.tab-content .tab-pane');
    let caller = {};
    console.log('I made it here 2');
    if ($A.generic.checkVariableType(panes) !== 'domelement') {
        throw Error('UI Error: Dom element for makeNewPane() not valid.');
    }

    //reset the tabs and panes so new tabs/panes can be added.
    tabs.innerHTML = '';
    panes.innerHTML = '';
    let isDefault = false;
    let i = 0;
    console.log('I made it here 3');

    data.forEach((itm) => {
        const tabKey = `WOWOitm-${itm.wowo_id}`;
        console.log('I made it here 3.5', tabKey);
        if (i === 0) {
            isDefault = true;
        }
        tabs.appendChild($A.app.makeNewTab(tabTemplate, tabKey, itm.name, isDefault));
        console.log('I made it here 3.75');
        panes.appendChild($A.app.makeNewPane(paneTemplate, tabKey, isDefault));
        i++;

        // finally, we define callbacks for each tab
        caller[tabKey] = async () => {
            $A.query().search('tata')
                .fields('tata_id', 'description', 'status', 'creator_id', 'assignee_id', 'deadline', 'tata_create_time')
                .where({
                    tawo_id: itm.wowo_id,
                    tata_delete_time: 'is null',
                })
                .order([
                    {tbl: 'tata', col: 'id', sort: 'desc'},
                ]).page(1, 1000).execute('workspacesDashboardResponse', createWorkSpaceDashboard, {key: tabKey, data: itm});
        }
        console.log('I made it here 5 iter');
    });

    console.log('I made it here 6');
    $A.dashboard('wsTabs', caller);
    console.log('I made it here 7');

    /**
     * Morphes Tasks data retrieved from the backend for specified WorkSpace, using lodash, 
     * and displays a Tasks dashboard.
     * 
     * @param {*} data: retrived from API call.
     * @param {str} containerId: DOM element id value.
     */
    function createWorkSpaceDashboard(tasks, responseContainerId, mapper) {
        const wsKey = mapper.key;
        const workspace = mapper.data;
        let container = document.querySelector('#pane-' + wsKey + ' #WSDB .backlog-col');

        if ($A.generic.checkVariableType(container) !== 'domelement') {
            throw Error('UI Error: createWorkSpaceDashboard() could not find valid shell for embed operation.');
        }

        const template = container.querySelector('.card');

        tasks.forEach((task) => {
            let clone = template.cloneNode(true);
            clone.classList.remove('d-none');
            console.log('I made it here 8');
            $A.app.embedData(task, clone, true);
            container.appendChild(clone);
        });
    }
}
