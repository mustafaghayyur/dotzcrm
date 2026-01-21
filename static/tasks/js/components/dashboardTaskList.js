import { Fetcher, defineRequest } from '../../../core/js/lib/async.js';
import helper from "../helper.js";

/**
 * Callback function for Fetcher() that maps retieved user's tasks to page elements.
 * @param {obj} data: results object from Fetcher call
 * @param {str} containerId: Id of the container to show any error messages.
 */
export default function (data, containerId) {
    const ulId = containerId.replace(/Response$/,'List');
    let ul = document.getElementById(ulId); // should be the ul parent node.
    let originalLiItem = ul.querySelector('li.list-group-item');
    ul.innerHTML = '';
    let li = null;
    
    if (Array.isArray(data)) {
        data.forEach(item => {
            li = originalLiItem.cloneNode(true);
            li.querySelector('.description').dataset.taskId = helper.forms.escapeHtml(item.tid);
            li.querySelector('.description').textContent = item.description || JSON.stringify(item);
            li.querySelector('.status').textContent = helper.forms.escapeHtml(item.status);
            li.querySelector('.tupdate_time').textContent = helper.dates.convertToDisplayLocal(item.tupdate_time);
            li.querySelector('.deadline').textContent = helper.dates.convertToDisplayLocal(item.deadline);
            ul.appendChild(li);
        });

        addListenersToTasks(ul);
    } else {
        originalLiItem.innerHTML = '<pre>' + helper.forms.escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        container.appendChild(originalLiItem);
    }

    /**
     * Adds read functionality to each fetched task.
     * Adds event listeners to the fetched tasks, allowing
     * for Task Details Modal to become operational on them.
     * @param {domelement} container - passed by TabbedDashBoard()
     */
    function addListenersToTasks(container){
        if(container instanceof HTMLElement){
            // implment listener and fetcher for item details modal...
            let tasks = container.querySelectorAll('.task-details-link');
            tasks.forEach(task => {
                let id = task.dataset.taskId;
                let request = defineRequest('api.tasks.crud', String(id));
                task.addEventListener('click', async ()=>{
                    const callback = await helper.tasks.load('taskDetails');
                    Fetcher(request, 'taskDetailsModalResponse', {}, callback);
                    helper.router().updateAddressBar('task_id', id);
                });
            });
        }
    }
}