import $A from "../helper.js";

/**
 * Our own Redux/State Manager
 * Not as sophisticated as ReactJS, but serves the purpose.
 */

// Registry to cache loaded fetch modules to avoid repeated imports
const fetchModuleRegistry = {};

// Internal state memory to persist key/mapper pairs during session (single session, no localStorage)
const stateMemory = new Map();


/**
 * Searches and stores in-memory, the fetch function component using fetchFile specified.
 * @param {*} componentName: fetch function shorthand 
 * @param {*} appName: current app/module/space 
 * @param {*} fetchFile: defauls to 'Default' suffix for fetch-file.
 * @returns fetchFunctionFullName
 */
async function findFetchComponent(componentName, appName, fetchFile) {
    const functionName = 'fetch' + componentName.charAt(0).toUpperCase() + componentName.slice(1);
    try {
        if (!fetchModuleRegistry[fetchFile]) {
            fetchModuleRegistry[fetchFile] = await $A.app.loadFetchModule(appName, fetchFile);
        }
        const func = fetchModuleRegistry[fetchFile][functionName];
    } catch (error) {
        throw Error('State Error: Could not import fetch component: ' + fetchFile + '.' + functionName + '. ' + error.message);
    }

    return functionName;
}

/**
 * Returns fetchFunction module component from memory.
 * 
 * @param {*} functionName: proper fetchFunction name
 * @param {*} fileName: file the function component resides in (default is 'Default')
 * @returns 
 */
function getFetchComponent(functionName, fileName) {
    try {
        return fetchModuleRegistry[fileName][functionName];
    } catch (error) {
        throw Error('State Error: Could not find fetch component: ' + fileName + '.' + functionName + '. ' + error.message);
    }
    
}

/**
 * Parses the state key into its four components.
 * @param {string} key - Unique key in string form that identifies one fetch 'state' for recurring triggering
 * @param {string} configString - configurations: 'appName.uniqueContainerIdentifier'
 * @returns {object} - { appName, containerId, componentFunctionName }
 */
function parseConfigString(key, configString) {
    const parts = configString.split('.');
    if (parts.length !== 2) {
        throw new Error(`State Error: Invalid state key format: "${configString}". Expected format: "appName.uniqueContainerIdentifier"`);
    }
    
    const [appName, componentName] = parts;
    const containerId = `${componentName}Response`;
    
    if (!appName || !containerId || !componentName) {
        throw new Error(`State Error: Cannot determine all required configuraton parts for key: "${key}". String provided: "${configString}"`);
    }
    
    return { appName, containerId, componentName };
}

/**
 * Updates the state with fetch function and its arguments, within 
 * in-memory storage for later retrieval via triggerState().
 * 
 * @param {string} key - The state key
 * @param {string} configString - configurations: 'appName.uniqueContainerIdentifier'
 * @param {obj} mapper - DIctionary of key => val pairs used as arguments passed to the fetch function
 * @returns {Promise<void>}
 */
async function updateState(key, configString, mapper = {}, fetchFile = 'Default') {
    const typeMapper = $A.generic.checkVariableType(mapper);
    if (typeMapper !== 'dictionary') {
        throw Error(`State Error: State mapper argument should be an Object. Received: ${typeMapper}.`);
    }
    
    try {
        const { appName, containerId,  componentName } = parseConfigString(key, configString);
        
        const fetchFunctionFullName = await findFetchComponent(componentName, appName, fetchFile);
        if (typeof fetchFunction !== 'function') {
            throw new Error(`State Error: Function "${fetchFunctionFullName}" not found in fetch module for app: "${appName}"`);
        }
        
        // store in memory with short-hand for key:value pairs...
        stateMemory.set(key, {
            appName,
            mapper,
            containerId,
            componentName,
            fetchFunctionFullName,
            fetchFile,
            timestamp: Date.now()
        });
    } catch (error) {
        console.error(`State Error: State update failed for key: "${key}"`, error);
        throw error;
    }
}

/**
 * Triggers a previously stored state by its key.
 * This executes the fetch function with the args that were stored when updateState() was called.
 * 
 * @param {string} key - The unique key for the state (first part of the state key)
 * @returns {Promise<void>}
 */
function triggerState(key, newMapper = {}) {
    if (!stateMemory.has(key)) {
        throw new Error(`State Error: No state found for key: "${key}". Call updateState() first to initialize this state.`);
    }
    try {
        const stateData = stateMemory.get(key);
        const { appName, mapper, containerId,  componentName, fetchFunctionFullName, fetchFile, timestamp } = stateData;
        
        let args = $A.generic.merge(mapper, newMapper)
        const page = $A.generic.getter(args, 'page', 1);
        args['page'] = $A.generic.checkVariableType(page) === 'number' ? page : 1;

        const fetchFunction = getFetchComponent(fetchFunctionFullName, fetchFile);
        if ($A.generic.checkVariableType(fetchFunction) !== 'function') {
            throw new Error(`State Error: Function "${fetchFunctionFullName}" not found in fetch module for app: "${appName}"`);
        }

        // Call the fetch function with the stored args
        return fetchFunction(args, containerId, componentName);
        
    } catch (error) {
        console.error(`State Error: State trigger failed for key: "${key}"`, error);
        throw error;
    }
}

/**
 * State Manager
 * 
 * Usage:
 * - update(key, 'appName.uniqueContainerIdentifier', [arg1, arg2, ...])
 *   Stores in state fetch function call.
 * 
 * - trigger('key')
 *   Executes the fetch function with previously stored args for that key.
 */
export default {
    save: updateState,
    trigger: triggerState,
    clearModuleCache: () => { Object.keys(fetchModuleRegistry).forEach(key => delete fetchModuleRegistry[key]); }
};

