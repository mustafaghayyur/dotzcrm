import $A from "../helper.js";


export default (data, containerId) => {
    let container = $A.app.containerElement(containerId);
    let tabs = container.querySelector('.nav-tabs');
    let panes = container.querySelector('.tab-content');
    let tabTemplate = container.querySelector('.nav-tabs .nav-item');
    let paneTemplate = container.querySelector('.tab-content .tab-pane');
    let caller = {};

    //reset the tabs and panes so new tabs/panes can be added.
    tabs.innerHTML = '';
    panes.innerHTML = '';

    data.forEach((itm) => {
        tabs.appendChild($A.app.makeNewTab(tabTemplate, `tab_${itm.wowo_id}_itm`, itm.name, isDefault));
        panes.appendChild($A.app.makeNewPane(paneTemplate, `pane_${itm.wowo_id}_itm`, isDefault));
        
        let current = panes.querySelector(`#pane_${itm.wowo_id}_itmContainer`);
        current.innerHTML = `<h6>${itm.name}</h6><div class="small">${itm.description}</div>`;

        // finally, we define callbacks for each tab
        caller[itm.wowo_id] = async () => {
            $A.query().search('tata')
                .fields('tata_id', 'description', 'status', 'creator_id', 'assignee_id', 'deadline')
                .where({
                    tawo_id: itm.wowo_id,
                    tata_delete_time: 'is null',
                })
                .order([
                    {tbl: 'tata', col: 'id', sort: 'desc'},
                ]).page(1, 1000).execute(`workspace${itm.wowo_id}DashboardResponse`, createWorkSpaceDashboard);
        }
    });

    $A.dashboard('wsTabs', {});

    /**
     * Morphes Tasks data retrieved from the backend for specified WorkSpace, using lodash, 
     * and displays a Tasks dashboard.
     * 
     * @param {*} data: retrived from API call.
     * @param {str} containerId: DOM element id value.
     */
    function createWorkSpaceDashboard(data, containerId) {
        data.forEach((itm) => {
            $A.app.embedData(itm, 'workspaceDashboardResponse');
        });
        
    }
}
