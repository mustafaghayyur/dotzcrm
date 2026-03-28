/**
 * Build a state of sorts that allows 'setting' a property: when property is set, what we mean is the following actions are taken:
 *  - property key is a string with four parts seperated by '.'
 *      - first part is an identifier (str) - unique key used in internal memory to preserve this instance
 *      - second part is a containerId (str)
 *      - third part is a component-identifyer (str)
 *      - fourth part is function-name without the 'fetch' prefix that is defined in any static/{app-name}/js/crud/fetch.js file
 *  - property value being passed, is an array of various arguments.
 * 
 *  - Much similar to examples seen throughout out our js/components/* we will attempt to use the key/value pairs to extract the elements and use them as such:
 * 
 *      invoke/call the `fetch{fourthPartOfKey}`() function that we have the string name of as such:
 *          fetch{fourthPartOfKey}([..arrOfValuePartsAsArgs], containerId, componentName)
 * 
 * 
 *  - The order of arguments passed to `fetch{fourthPartOfKey}`() is not important, you can have the array of arguments passed last if that helps you
 * 
 * Purpose & State Persistence:
 * -----------------------------------
 * We wish to imitate ReactJS in their state redux. When the 'state' is updated with key/value pairs, we call the js/crud/fetch.js functions.
 * The state key/value pairs are stored in in-memory storage (single session, no localStorage) so they can be re-triggered later.
 * 
 * Usage:
 * - $A.state.updateState('myId.myContainerId.tasksItem.todosDashboard', [arg1, arg2, ...])
 *   Stores the state and executes the fetch function.
 * 
 * - $A.state.triggerState('myId')
 *   Re-executes the fetch function with the previously stored args for that identifier.
 * 
 * I will of course add this lib to the $A library myself, I just need you to design this lib as best you can.
 */

// Registry to cache loaded fetch modules to avoid repeated imports
const fetchModuleRegistry = {};

// Internal state memory to persist key/args pairs during session (single session, no localStorage)
const stateMemory = new Map();

/**
 * Dynamically loads a fetch module for a given app.
 * @param {string} appName - The app name (e.g., 'tasks', 'customers')
 * @returns {Promise<object>} - The fetch module exports
 */
async function loadFetchModule(appName) {
    if (fetchModuleRegistry[appName]) {
        return fetchModuleRegistry[appName];
    }
    
    try {
        const module = await import(`../../${appName}/js/crud/fetch.js`);
        fetchModuleRegistry[appName] = module;
        return module;
    } catch (error) {
        console.error(`Failed to load fetch module for app: ${appName}`, error);
        throw new Error(`Fetch module not found for app: ${appName}`);
    }
}

/**
 * Converts a string function name to camelCase with 'fetch' prefix.
 * e.g., 'TodosDashboard' -> 'fetchTodosDashboard'
 * @param {string} functionName - The function name without 'fetch' prefix
 * @returns {string} - The full function name with 'fetch' prefix
 */
function buildFunctionName(functionName) {
    return 'fetch' + functionName.charAt(0).toUpperCase() + functionName.slice(1);
}

/**
 * Parses the state key into its four components.
 * @param {string} key - The key in format 'identifier.containerId.componentName.functionName'
 * @returns {object} - { identifier, containerId, componentName, functionName, appName }
 */
function parseStateKey(key) {
    const parts = key.split('.');
    if (parts.length !== 4) {
        throw new Error(`Invalid state key format: "${key}". Expected format: "identifier.containerId.componentName.functionName"`);
    }
    
    const [identifier, containerId, componentName, functionName] = parts;
    
    // Extract app name from componentName (e.g., 'tasksItem' -> 'tasks')
    const appNameMatch = componentName.match(/^[a-z]+/);
    const appName = appNameMatch ? appNameMatch[0] : null;
    
    if (!appName) {
        throw new Error(`Cannot determine app name from component name: "${componentName}". Component names should start with app name in lowercase.`);
    }
    
    return { identifier, containerId, componentName, functionName, appName };
}

/**
 * Updates the state and triggers the corresponding fetch function.
 * Also persists the state in in-memory storage for later retrieval via triggerState().
 * 
 * Key format: 'identifier.containerId.componentName.functionName'
 * Value: array of arguments to pass to the fetch function
 * 
 * @param {string} key - The state key
 * @param {Array} args - The arguments to pass to the fetch function
 * @returns {Promise<void>}
 */
async function updateState(key, args) {
    // Validate arguments
    if (!Array.isArray(args)) {
        console.warn(`State argument should be an array. Received: ${typeof args}. Wrapping in array.`);
        args = [args];
    }
    
    try {
        const { identifier, containerId, componentName, functionName, appName } = parseStateKey(key);
        const fullFunctionName = buildFunctionName(functionName);
        
        // Load the fetch module for the app
        const fetchModule = await loadFetchModule(appName);
        
        // Get the fetch function from the module
        const fetchFunction = fetchModule[fullFunctionName];
        
        if (typeof fetchFunction !== 'function') {
            throw new Error(`Function "${fullFunctionName}" not found in fetch module for app: "${appName}"`);
        }
        
        // Store the state in internal memory for later re-triggering via triggerState()
        stateMemory.set(identifier, {
            key,
            args,
            containerId,
            componentName,
            functionName,
            appName,
            fullFunctionName,
            timestamp: Date.now()
        });
        
        // Call the fetch function with spread args, followed by containerId and componentName
        await fetchFunction(...args, containerId, componentName);
        
    } catch (error) {
        console.error(`State update failed for key: "${key}"`, error);
        throw error;
    }
}

/**
 * Re-triggers a previously stored state by its identifier.
 * This re-executes the fetch function with the args that were stored when updateState() was called.
 * 
 * @param {string} identifier - The unique identifier for the state (first part of the state key)
 * @returns {Promise<void>}
 */
async function triggerState(identifier) {
    if (!stateMemory.has(identifier)) {
        throw new Error(`No state found for identifier: "${identifier}". Call updateState() first to initialize this state.`);
    }
    
    try {
        const stateData = stateMemory.get(identifier);
        const { args, containerId, componentName, appName, fullFunctionName } = stateData;
        
        // Load the fetch module for the app
        const fetchModule = await loadFetchModule(appName);
        
        // Get the fetch function from the module
        const fetchFunction = fetchModule[fullFunctionName];
        
        if (typeof fetchFunction !== 'function') {
            throw new Error(`Function "${fullFunctionName}" not found in fetch module for app: "${appName}"`);
        }
        
        // Call the fetch function with the stored args
        await fetchFunction(...args, containerId, componentName);
        
    } catch (error) {
        console.error(`State trigger failed for identifier: "${identifier}"`, error);
        throw error;
    }
}

/**
 * State Manager - main export
 * 
 * Usage:
 * - updateState('identifier.containerId.componentName.functionName', [arg1, arg2, ...])
 *   Stores the state and executes the fetch function immediately.
 * 
 * - triggerState('identifier')
 *   Re-executes the fetch function with previously stored args for that identifier.
 */
export default {
    updateState: updateState,
    triggerState: triggerState,
    clearModuleCache: () => { Object.keys(fetchModuleRegistry).forEach(key => delete fetchModuleRegistry[key]); }
};

