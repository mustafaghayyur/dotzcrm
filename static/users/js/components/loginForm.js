import { Fetcher, defineRequest } from '../../../core/js/lib/async.js';
import helper from '../helper.js';

export default () => {
    const form = document.getElementById('loginForm');
    const submit = form.querySelector('.form-submit');

    submit.addEventListener('click', (e) => {
        e.preventDefault();
        const dictionary = helper.tasks.forms.generateDictionaryFromForm('loginForm');
        console.log('What is the dictionary looking like? ', dictionary);

        const request = defineRequest('auth.login', '', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': 'Bearer <access_token>',
            },
            credentials: 'same-origin',
            body: JSON.stringify(dictionary),
        });
        console.log('Heloooooooo3');
        Fetcher(request, 'authenticationResponse', {}, (data, containerId) => {
            console.log('Heloooooooo1');
            let urls = helper.app.memFetch('allowed_routes', true);
            console.log('checking login if urls are coming correctly...', urls);
            window.location.href = urls.ui.apps.tasks;
        });
    });
}