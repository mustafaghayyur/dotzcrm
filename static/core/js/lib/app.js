import { Fetcher, defineRequest } from "./async.js";
import generic from "../helpers/generic.js";
import app from "../helpers/app.js";
/**
 * The APP Module/Library allows for a centeral container for eeach 'app'/core of the 
 * Dotz CRM + PM Software.
 */

export function Main(callbackFunction) {
    document.addEventListener('DOMContentLoaded', () => {
        const request = defineRequest('auth.settings');
        Fetcher(request, 'authenticationResponse', {}, (data, containerId) => {
            generic.loopObject(data, (key, val) => {
                app.memSave(key, data[key]);
                console.log(`inside Main() saving settings ... Key: ${key}, Value: `, data[key]);
            });

            const loginRequired = document.getElementById('loginRequired');
            app.memSave('loginRequired', loginRequired.dataset.loginRequired);
            if (!data.is_authenticated && loginRequired.dataset.loginRequired === 'true') {
                relocateToLogin();
            }

            if (typeof callbackFunction === 'function') {
                return callbackFunction();
            }
        });
    });

    function relocateToLogin() {
        let urls = app.memFetch('allowed_routes', true);
        console.log('We have made it to relocateToLogiN! What is urls looking like?', urls);
        window.location.href = urls.ui.auth.login;
    }
}