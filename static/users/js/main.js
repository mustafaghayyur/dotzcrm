import { Fetcher, defineRequest } from "../../core/js/lib/async.js";
//import { TabbedDashBoard } from "../../core/js/lib/dashboard.js";
//import { showModal } from "../../core/js/lib/modal_linking.js";
import { Main } from '../../core/js/lib/app.js';
import helper from './helper.js';
import loginForm from "./components/loginForm.js";
//import { TasksO2OKeys } from "./constants.js";


Main(async () => {
    const liginForm = await helper.app.load('loginForm', 'users');
    loginForm();
    //Routes.add('task_id').modal('taskDetailsModal').component(helper.tasks.load('taskDetails'));
});
