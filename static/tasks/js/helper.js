import generic from '../../core/js/helpers/generic.js';
import app from '../../core/js/helpers/app.js';
import forms from '../../core/js/helpers/forms.js';
import dates from '../../core/js/helpers/dates.js';
import formsLocal from './helpers/forms.js';
import router from '../../core/js/lib/router.js';
//import validators from './helpers/validate.js';

/**
 * Assembles all core and tasks 'helpers' libraries into one callable helper object.
 */
export default {
    generic: generic,
    app: app,
    forms: forms,
    dates: dates,
    tasks: {
        forms: formsLocal,
        validators: null,
        
        /**
         * Loads a compoenent specified with argument.
         * @param {str} component: name of specific component. Components in sub-folders should be denoted with a 'subfolder.compoenentName'
         */
        load: (commponent) => {
            return app.load(commponent, 'tasks');
        }
    },
    router: router
};
