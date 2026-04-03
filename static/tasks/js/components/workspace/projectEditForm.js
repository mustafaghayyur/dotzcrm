import $A from "../../helper.js";
import { UpdateWorkSpace, CreateWorkSpace, UpdateDepartmentsInWorkSpace, UpdateLeaderInWorkSpace, AddDepartmentsToWorkSpace, AddLeaderToWorkSpace } from '../../crud/workspaces.js';

/**
 * Enabled all features in Task Edit Form.
 * 
 * @param {obj|str} taskInfo: full task record to edit | or string carrying current workspace_id
 */
export default (wowoData) => {
    let container = $A.dom.obtainElementCorrectly('workSpaceEditModal');
    let deptsField = $A.dom.searchElementCorrectly('form select[name="department_id"]', container);

    // Prefill form with workspace data if provided
    if ($A.generic.checkVariableType(wowoData) === 'dictionary') {
        $A.forms.prefillForms(wowoData, 'workSpaceEditForm');
    }

    $A.app.handleScreenSizeAdjustments($A.data.screens.sm, () => {
        // make some room for keyboard in mobile views...
        let form = $A.dom.searchElementCorrectly('form', container);
        let bufferDiv = $A.dom.makeDomElement('div', '', 'buffer');
        form.insertAdjacentElement('afterend', bufferDiv);
    });

    // departments list for workspace...
    $A.query().search('dede').fields('dede_id', 'name').order([{tbl:'dede', col: 'id', sort: 'desc'}])
        .execute('workSpaceEditModalResponse', embedDepartmentsDataIntoForm);


    // Save Operations Setup (Edit WorkSpace Modal)...
    const editTaskSaveBtn = $A.dom.obtainElementCorrectly('workSpaceEditFormSaveBtn');
    const wowo_id = $A.dom.searchElementCorrectly('#workSpaceEditForm input[name="wowo_id"]', container);
    $A.app.wrapEventListeners(editTaskSaveBtn, 'data-workspace-id', wowo_id.value, 'click', (e) => {
        e.preventDefault();
        const wowoId = e.currentTarget.getAttribute('data-workspace-id');
        if ($A.generic.isVariableEmpty(wowoId)) {
            CreateWorkSpace('workSpaceEditForm');
        } else {
            UpdateWorkSpace('workSpaceEditForm');
        }
    });

    // handle modal close confirmation...
    $A.app.wrapEventListeners(container, 'null', null, 'hide.bs.modal', (e) => {
        if (!$A.forms.confirm('close WorkSpace Edit Panel', 'Any unsaved data will be lost.')) {
            e.preventDefault();
            return null;
        }
    });

    /**
     * Embeds the data from query into form Select Fields.
     * For Department Ids
     * @param {obj} data 
     * @param {str} containerId 
     */
    function embedDepartmentsDataIntoForm(data, containerId) {
        let container = $A.dom.containerElement(containerId);
        let select = container.querySelector('form select[name="department_id"]');

        if ($A.generic.checkVariableType(select) !== 'domelement') {
            throw Error('Error FB004: Cannot find Department Select Field.');
        }

        if ($A.generic.checkVariableType(data) !== 'list') {
            throw Error('Error FB005: Cannot parse data object.');
        }

        data.forEach((itm) => {
            let elem = $A.dom.makeDomElement('option');
            elem.textContent = itm.name;
            elem.value = itm.dede_id;
            select.appendChild(elem);
        });
    }

}
