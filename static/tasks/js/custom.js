import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher } from "../../core/js/async.js";

/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */

document.addEventListener('DOMContentLoaded', TabbedDashBoard('Hello Motto'));

/**
    tickets = document.getElementsByClassName('ticket-details-link')
    tickets.forEach(ticket => {
        let info = dataset.ticketId
        console.log('checking values in ticketlinks:', dataset, dataset.ticketId)
        ticket.addEventListener('click', (info) => {
                triggerTicketDetailsGet(info)
            });
        });


    
*/
