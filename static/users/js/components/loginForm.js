import helper from '../helper.js';

export default () => {
    const form = document.getElementById('loginForm');
    const submit = form.querySelector('.form-submit');

    submit.addEventListener('click', (e) => {
        e.preventDefault();
        const dictionary = helper.forms.formToDictionary('loginForm');
        const request = helper.fetch.route('api.auth.login', '', { 
            method: 'POST',
            body: JSON.stringify(dictionary),
        });
        helper.fetch.body(request, 'authenticationResponse', {}, (data, containerId) => {
            let urls = helper.app.memFetch('allowed_routes', true);
            window.location.href = urls.ui.apps.tasks;
        });
    });
}