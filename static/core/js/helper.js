import generic from './helpers/generic.js';
import app from './helpers/app.js';
import forms from './helpers/forms.js';
import dates from './helpers/dates.js';
import { showModal, updateUrlParam } from './lib/router.js';
import { Fetcher, defineRequest } from './lib/async.js';
import { Editor } from './lib/editor.js';
import { TabbedDashBoard } from './lib/dashboard.js';

/**
 * Assembles all core and tasks 'helpers' libraries into one callable helper object.
 */
export default {
    generic: generic,
    app: app,
    forms: forms,
    dates: dates,
    router: { 
        create: showModal,
        update: updateUrlParam
    },
    fetch: {
        route: defineRequest,
        body: Fetcher
    },
    editor: {
        make: Editor
    },
    dashboard: TabbedDashBoard,
};
