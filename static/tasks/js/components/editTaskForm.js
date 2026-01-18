import helper from "../../../core/js/helpers/main";


    // Edit Task Modal: Save Operations Setup...
    const editTaskSaveBtn = document.getElementById('taskEditFormSaveBtn');
    editTaskSaveBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const tid = document.querySelector('#taskEditForm input[name="tid"]');
        if (!(tid instanceof HTMLElement)) {
            throw Error('Cannot find `tid` field, unable to perform edit/create operation.');
        }
        if(tid.value){
            UpdateTask('taskEditForm');
        }else{
            CreateTask('taskEditForm');
        }
    });