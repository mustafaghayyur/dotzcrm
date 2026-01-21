import $A from '../helper.js';

export default () => {
    const form = document.getElementById('loginForm');
    const submit = form.querySelector('.form-submit');

    submit.addEventListener('click', (e) => {
        e.preventDefault();
        const dictionary = $A.forms.formToDictionary('loginForm');
        const request = $A.fetch.route('api.auth.login', '', { 
            method: 'POST',
            body: JSON.stringify(dictionary),
        });
        $A.fetch.body(request, 'authenticationResponse', {}, (data, containerId) => {
            let urls = $A.app.memFetch('allowed_routes', true);
            window.location.href = urls.ui.apps.tasks;
        });
    });
}