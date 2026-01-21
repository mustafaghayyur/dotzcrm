import helper from "../helper.js";

export default () => {
    // add 'clean form' functionality to all .open-form btns...
    const TasksO2OKeys = helper.tasks.data['TasksO2OKeys'];
    const openFormBtn = document.querySelectorAll('.open-form');
    openFormBtn.forEach(button => {
        button.addEventListener('click', () => {
            helper.tasks.forms.cleanTaskForm('taskEditForm', TasksO2OKeys);
        });
    });
}