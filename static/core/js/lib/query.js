import $A from "../helper.js";


export default function () {
    let tbl = null;
    let selectors = [];
    let conditions = {};
    let joins = {};
    let ordering = [];
    let count = null;
    let page = null;
    const routes = {
        'list-o2o': 'api.terminal.list',
        'list-rlc': 'api.terminal.listrlc',
        'list-m2m': 'api.terminal.listm2m',
        'crud-o2o': 'api.terminal.crud',
        'crud-rlc': 'api.terminal.crudrlc',
        'crud-m2m': 'api.terminal.crudm2m',
    };
    let params = null;
    let chosenRoute = null;
    let errors = [];

    

    const kernel = {
        search: (tblKey, type = 'list-o2o') => {
            if ($A.generic.checkVariableType(tblKey) !== 'string' || $A.generic.isVariableEmpty(tblKey)) {
                throw Error('search() requires table-key argument.');
            }
            if ($A.generic.checkVariableType(type) !== 'string' || $A.generic.isVariableEmpty(type) || !(type in routes)) {
                throw Error('search() requires type argument to be string enum of ["list-o2o" | "list-m2m" | "list-rlc"].');
            }
            tbl = tblKey;
            chosenRoute = type
            return kernel;
        },

        create: (type = 'crud-o2o') => {
            
            if ($A.generic.checkVariableType(type) !== 'string' || $A.generic.isVariableEmpty(type) || !(type in routes)) {
                throw Error('search() requires type argument to be string enum of ["crud-o2o" | "crud-m2m" | "crud-rlc"].');
            }
            return kernel;
        },

        edit: (type = 'crud-o2o') => {
            
            if ($A.generic.checkVariableType(type) !== 'string' || $A.generic.isVariableEmpty(type) || !(type in routes)) {
                throw Error('search() requires type argument to be string enum of ["crud-o2o" | "crud-m2m" | "crud-rlc"].');
            }
            return kernel;
        },

        delete: (type = 'crud-o2o') => {
            
            if ($A.generic.checkVariableType(type) !== 'string' || $A.generic.isVariableEmpty(type) || !(type in routes)) {
                throw Error('search() requires type argument to be string enum of ["crud-o2o" | "crud-m2m" | "crud-rlc"].');
            }
            return kernel;
        },

        single: (type = 'crud-o2o') => {
           
            if ($A.generic.checkVariableType(type) !== 'string' || $A.generic.isVariableEmpty(type) || !(type in routes)) {
                throw Error('search() requires type argument to be string enum of ["crud-o2o" | "crud-m2m" | "crud-rlc"].');
            }
            return kernel;
        },

        fields: (...args) => {
            if ($A.generic.checkVariableType(args) !== 'list' || $A.generic.isVariableEmpty(args)) {
                throw Error('search().fields() requires atleast one argument.');
            }
            selectors = args;
            return kernel;
        },

        where: (dictionary) => {
            if ($A.generic.checkVariableType(dictionary) !== 'dictionary') {
                throw Error('search().where() requires a dictionary of values.');
            }
            conditions = dictionary;
            return kernel;
        },

        join: (dictionary) => {
            if ($A.generic.checkVariableType(dictionary) !== 'dictionary') {
                throw Error('search().join() requires a dictionary of values.');
            }
            joins = dictionary;
            return kernel;
        },

        order: (orderByList) => {
            if ($A.generic.checkVariableType(orderByList) !== 'list') {
                throw Error('search().order() requires a list of dictionaries containing "tbl", "col", "sort" keys.');
            }
            ordering = orderByList;
            return kernel;
        },

        page: (pageNumber, perPage = 20) => {
            if ($A.generic.checkVariableType(pageNumber) !== 'number' || $A.generic.checkVariableType(perPage) !== 'number') {
                throw Error('search().page() requires pageNumber and perPage to both be numerical (integer) values.');
            }
            if (pageNumber < 1 || perPage < 1) {
                throw Error('search().page() requires pageNumber and perPage to both be a value greater than 0.');
            }
            count = perPage;
            page = pageNumber;
            return kernel;
        },

        /**
         * Internal function.
         */
        cleanMemory: () => {
            tbl = null;
            selectors = [];
            conditions = {};
            joins = {};
            ordering = [];
            count = null;
            page = null;
        },

        execute: () => {
            // error check inputs... then:
            
            $A.fetch.route(routes[chosenRoute], params, { method: 'POST', body: JSON.stringify(dictionary) });
            $A.fetch.body(request, responseContainer, mapper, callbackFunction);
            kernel.cleanMemory();
        }
    } 

    function assembleSearchParams() {
        return {
            tbl: tbl,
            selectors: selectors,
            conditions: conditions,
            ordering: ordering,
            joins: joins,
            limit: [count, page]
        }
    }
    //return the kernal...
    return kernel;
}

