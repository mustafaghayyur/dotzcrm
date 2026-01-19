import generic from '../../core/js/helpers/generic.js';
import forms from '../../core/js/helpers/forms.js';
import dates from '../../core/js/helpers/dates.js';
import formsLocal from './helpers/forms.js';
//import validators from './helpers/validate.js';

/**
 * Assembles all core and tasks 'helpers' libraries into one callable helper object.
 */
export default {
    generic: generic,
    forms: forms,
    dates: dates,
    tasks: {
        forms: formsLocal,
        validators: null,
        
        /**
         * Loads a compoenent specified with argument.
         * @param {str} component: name of specific component. Components in sub-folders should be denoted with a 'subfolder.compoenentName'
         */
        //load: generic.load(commponent, 'tasks')
    }
};
