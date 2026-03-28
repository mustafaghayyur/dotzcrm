import $A from "../helper.js";

/**
 * Our own Redux/State Manager
 * Not as sophisticated as ReactJS, but serves the purpose.
 */

// Registry to cache loaded fetch modules to avoid repeated imports
const fetchModuleRegistry = {};

// Internal state memory to persist key/args pairs during session (single session, no localStorage)
const stateMemory = new Map();

/**
 * Formulates valid function Name, loads function module file, 
 * and returns requested function component.
 * 
 * @param {*} funcName: short-hand function name (without 'fetch' prefix)
 * @param {*} fileName: file the function component resides in (default is 'Default')
 * @returns 
 */
function fetchComponent(funcName, appName, fileName) {
    const functionName = 'fetch' + funcName.charAt(0).toUpperCase() + funcName.slice(1);
    if (!fetchModuleRegistry[fileName]) {
        fetchModuleRegistry[functionName] = $A.app.loadFetchModule(appName, fileName);
    }
    try {
        return fetchModuleRegistry[fileName].functionName;
    } catch (error) {
        throw Error('State Error: Could not import fetch component: ' + fileName + '.' + functionName + '. ' + error.message);
    }
}

/**
 * Parses the state key into its four components.
 * @param {string} key - The key in format 'identifier.containerId.componentName.functionName'
 * @returns {object} - { identifier, containerId, componentName, functionName, appName }
 */
function parseConfigString(identifier, configString) {
    const parts = key.split('.');
    if (parts.length !== 4) {
        throw new Error(`State Error: Invalid state key format: "${key}". Expected format: "identifier.containerId.componentName.functionName"`);
    }
    
    // , containerId, callbackFunctionName, 
    const [appName, containerId, callbackFunctionName, fetchFunctionName] = parts;
    
    if (!appName || !containerId || !callbackFunctionName || !fetchFunctionName) {
        throw new Error(`State Error: Cannot determine all four required configuraton parts for key: "${identifier}". String provided: "${configString}"`);
    }
    
    return { appName, containerId, callbackFunctionName, fetchFunctionName };
}

/**
 * Updates the state with fetch function and its arguments, within 
 * in-memory storage for later retrieval via triggerState().
 * 
 * @param {string} identifier - The state key
 * @param {string} configString - configurations: 'app.containerId.componentName.functionName'
 * @param {Array} args - Array of additional arguments to pass to the fetch function
 * @returns {Promise<void>}
 */
async function updateState(identifier, configString, args, fetchFile = 'Default') {
    if (!Array.isArray(args)) { // Validate arguments
        console.warn(`State Error: State argument should be an array. Received: ${typeof args}. Wrapping in array.`);
        args = [args];
    }
    
    try {
        const { appName, containerId, callbackFunctionName, fetchFunctionName } = parseConfigString(configString);
        const fetchFunction = await fetchComponent(fetchFunctionName, appName, fetchFile);
        
        if (typeof fetchFunction !== 'function') {
            throw new Error(`State Error: Function "${fullFunctionName}" not found in fetch module for app: "${appName}"`);
        }
        
        // store in memory with short-hand for key:value pairs...
        stateMemory.set(identifier, {
            appName,
            args,
            containerId,
            callbackFunctionName,
            fetchFunction,
            timestamp: Date.now()
        });
    } catch (error) {
        console.error(`State Error: State update failed for key: "${key}"`, error);
        throw error;
    }
}

/**
 * Triggers a previously stored state by its identifier.
 * This executes the fetch function with the args that were stored when updateState() was called.
 * 
 * @param {string} identifier - The unique identifier for the state (first part of the state key)
 * @returns {Promise<void>}
 */
async function triggerState(identifier) {
    if (!stateMemory.has(identifier)) {
        throw new Error(`State Error: No state found for identifier: "${identifier}". Call updateState() first to initialize this state.`);
    }
    try {
        const stateData = stateMemory.get(identifier);
        const { appName, args, containerId, callbackFunctionName, fetchFunction } = stateData;
        
        if (typeof fetchFunction !== 'function') {
            throw new Error(`State Error: Function "${fullFunctionName}" not found in fetch module for app: "${appName}"`);
        }

        // Call the fetch function with the stored args
        return await fetchFunction(...args, containerId, callbackFunctionName);
        
    } catch (error) {
        console.error(`State Error: State trigger failed for identifier: "${identifier}"`, error);
        throw error;
    }
}

/**
 * State Manager
 * 
 * Usage:
 * - update(identifier, 'app.containerId.componentName.functionName', [arg1, arg2, ...])
 *   Stores in state fetch function call.
 * 
 * - trigger('identifier')
 *   Executes the fetch function with previously stored args for that identifier.
 */
export default {
    save: updateState,
    trigger: triggerState,
    clearModuleCache: () => { Object.keys(fetchModuleRegistry).forEach(key => delete fetchModuleRegistry[key]); }
};

