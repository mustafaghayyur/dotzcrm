import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper } from "./mappers.js";
/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */



// implment dashboard on index.html
document.addEventListener('DOMContentLoaded', TabbedDashBoard(addListenersToTasks));



function addListenersToTasks(container){
    if(container instanceof HTMLElement){
        // implment listener and fetcher for item details modal...
        let tasks = container.querySelectorAll('.task-details-link');
        tasks.forEach(task => {
            // @todo - find a way to correctly refeeence taskid data attribute
            let id = task.dataset.taskid;
            request = defineRequest('rest/tasks/crud/' + id);
            
            task.addEventListener('click', Fetcher(request, 'ticketDetailsModal', {}, taskDetailsMapper));
        });
    }
}
