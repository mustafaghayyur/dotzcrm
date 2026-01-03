/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */
import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper } from "./mappers.js";

// implment dashboard on index.html
document.addEventListener(
    'DOMContentLoaded', 
    TabbedDashBoard(addListenersToTasks)
);

/**
 * This is a callback that adds event listeners to the fetched tasks, allowing
 * for Task Details Modal to become operational on them.
 * @param {domelement} container - passed by TabbedDashBoard()
 */
function addListenersToTasks(container){
    if(container instanceof HTMLElement){
        // implment listener and fetcher for item details modal...
        let tasks = document.querySelectorAll('.task-details-link');
        tasks.forEach(task => {
            let id = task.dataset.taskId;
            let request = defineRequest('/rest/tasks/crud/' + id);
            task.addEventListener('click', ()=>{
                Fetcher(request, 'ticketDetailsModalResponse', {}, taskDetailsMapper)
            });
        });
    }
}
