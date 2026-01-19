import { Fetcher, defineRequest } from '../../../core/js/lib/async.js';
import helper from '../helper.js';

export default () => {
    const form = document.getElementById('loginForm');
    const submit = form.querySelector('.form-submit');

    submit.addEventListener('click', () => {
        const dictionary = helper.tasks.forms.generateDictionaryFromForm('loginForm');
        const request = defineRequest('auth.login', '', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': 'Bearer <access_token>',
            },
            credentials: 'same-origin',
            body: JSON.stringify(dictionary),
        });
        Fetcher(request, 'authenticationResponse', {}, () => {
            window.location.href = helper.routes.dashboard;
            window.location.reload();
        });
    });
}