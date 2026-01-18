/**
 * The APP Module/Library allows for a centeral container for eeach 'app'/core of the 
 * Dotz CRM + PM Software.
 */

export function Main(callbackFunction) {
    document.addEventListener('DOMContentLoaded', () => {
        if (typeof callbackFunction === 'function') {
            return callbackFunction();
        }
    });
}