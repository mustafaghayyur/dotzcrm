import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper } from "./mappers.js";
/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */

// implment dashboard on index.html
document.addEventListener('DOMContentLoaded', TabbedDashBoard('Hello Motto'));

// implment listener and fetcher for item details modal...
let tasks = document.getElementsByClassName('task-details-link');
tasks.forEach(task => {
    let id = dataset.taskid;
    request = defineRequest('rest/tasks/crud/' + id);
    
    task.addEventListener('click', Fetcher(request, 'ticketDetailsModal', {}, taskDetailsMapper));
});

