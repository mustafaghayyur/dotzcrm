import $A from "../../helper.js";

/**
 * Handles current state of user watching task
 * 
 * @param {arr} data: api data 
 * @param {str} containerId 
 */
export default function(data, containerId) {
    let constainer = $A.dom.containerElement(containerId);
    let watchBtn = $A.dom.seachElementCorrectly('addWatcher', constainer);
    let unwatchBtn = $A.dom.seachElementCorrectly('removeWatcher', constainer);

    if ($A.generic.isVariableEmpty(data)) {
        watchBtn.classList.remove('d-none');
        unwatchBtn.classList.add('d-none');
    } else {
        unwatchBtn.classList.remove('d-none');
        watchBtn.classList.add('d-none');
    }

    // add event listeners of watch buttons...
    $A.app.eventListener('click', watchBtn, async (e) => {
        e.preventDefault();
        const taskId = e.currentTarget.dataset.listenerData.task_id;
        $A.state.crud.create('tawa', { task_id: taskId }, container, (resp, conId) => {
            watchBtn.classList.add('d-none');
            unwatchBtn.classList.remove('d-none');
            $A.app.generateResponseToAction(conId, 'Added to watcher list.');
        });
    }, {'task_id': data.task_id});

    $A.app.eventListener('click', unwatchBtn, async (e) => {
        e.preventDefault();
        const taskId = e.currentTarget.dataset.listenerData.task_id;
        $A.state.crud.delete('tawa', { task_id: taskId }, container, (resp, conId) => {
            watchBtn.classList.remove('d-none');
            unwatchBtn.classList.add('d-none');
            $A.app.generateResponseToAction(containerId, 'Removed from watcher list.');
        });
    }, {'task_id': data.task_id});
}