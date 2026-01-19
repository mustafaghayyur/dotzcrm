import { Fetcher, defineRequest } from "./async.js";

/**
 * The APP Module/Library allows for a centeral container for eeach 'app'/core of the 
 * Dotz CRM + PM Software.
 */

export function Main(callbackFunction) {
    document.addEventListener('DOMContentLoaded', () => {
        
        const request = defineRequest('auth.settings', '', { 
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': 'Bearer <access_token>',
            },
            credentials: 'same-origin',
            //body: JSON.stringify(dictionary),
        });
        Fetcher(request, 'authenticationResponse', {}, () => {
            if (typeof callbackFunction === 'function') {
                return callbackFunction();
            }
        });
    });
}