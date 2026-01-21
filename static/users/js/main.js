import { Main } from '../../core/js/lib/app.js';
import helper from './helper.js';

/**
 * Main will load the App for Users module/space.
 */
Main(async () => {
    const liginForm = await helper.app.load('loginForm', 'users');
    loginForm(); // load login form functionaility
});
