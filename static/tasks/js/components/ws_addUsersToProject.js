import $A from "../helper.js";
import { UpdateWorkSpace, CreateWorkSpace, UpdateDepartmentsInWorkSpace, UpdateLeaderInWorkSpace, AddDepartmentsToWorkSpace, AddLeaderToWorkSpace } from '../crud/workspaces.js';

/**
 * Handles Adding Team Members/Leaders to WorkSpace
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
    $A.query().search('wode').fields('wode_id', 'dede_name').order([{tbl:'wode', col: 'id', sort: 'desc'}])
        .execute('nulnull', embedDepartmentsDataIntoForm);

    $A.app.wrapEventListeners(deptsField, 'data-current-depts', null, 'change', (e) => {
        let depts = Array.from(e.currentTarget.selectedOptions);
        const currentDepts = depts.map(option => option.value);
        if ($A.generic.checkVariableType(currentDepts) === 'list' && currentDepts.length > 0) {
            $A.query().search('usus').fields('usus_id', 'username', 'first_name', 'last_name'
                ).join({
                    'left|usus_id': 'deus_user_id',
                }).where({
                    deus_department_id: currentDepts,
                    user_level: [10, 20, 30, 40, 50] // + $A.data.user.levels.leader // @todo: add gt/lt operators to conditions
                }).order([
                    {tbl:'usus', col: 'last_name', sort: 'asc'},
                    {tbl:'usus', col: 'first_name', sort: 'asc'}
                ]).page(1, 1000)
                .execute('workSpaceEditModalResponse', embedUsersDataIntoForm);
        }
    });

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
        if (!$A.forms.confirm('close WorkSpace Users Panel', 'Any unsaved data will be lost.')) {
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



    /**
     * Embeds the data from query into form Select Fields.
     * For User Ids (Team Leader)
     * @param {obj} data 
     * @param {str} containerId 
     */
    function embedUsersDataIntoForm(data, containerId) {
        let container = $A.dom.containerElement(containerId);
        let select = container.querySelector('form select[name="lead_id"]');

        if ($A.generic.checkVariableType(select) !== 'domelement') {
            throw Error('Error FB001: Cannot find Team Leader Select Field.');
        }

        if ($A.generic.checkVariableType(data) !== 'list') {
            throw Error('Error FB003: Cannot parse data object.');
        }

        // reset form...
        select.innerHTML = '';
        const users = removeDuplicateUsers(data);
        console.log('These are users post remoaveUsersDup()', users);

        users.forEach((itm) => {
            let elem = $A.dom.makeDomElement('option');
            elem.textContent = `${itm.first_name} ${itm.last_name} (@${itm.username})`;
            elem.value = itm.usus_id;
            select.appendChild(elem);
        });
    }
    
    function removeDuplicateUsers(usersList) {
        if (!$A.generic.checkVariableType(usersList) === 'list') {
            return [];
        }
        console.log('Inside removeDuplaicteUsers()', usersList);
        const seen = new Set();
        const finalList = usersList.filter((user) => {
            if (!$A.generic.checkVariableType(user) === 'dictionary') {
                console.log('1 removing user with id: ', user);
                return false;
            }
            if (user.usus_id == null) {
                console.log('2 removing user with id: ', user);
                return false;
            }

            if (seen.has(user.usus_id)) {
                console.log('3 removing user with id: ', user);
                return false;
            }

            seen.add(user.usus_id);
            return true;
        });
        return finalList;
    }
}
