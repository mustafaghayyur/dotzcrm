import $A from "../helper.js";

/**
 * Carries operations enabling State and UX features
 */
export default {
    triggerAllForTable: function(tbl, container) {
        if ($A.generic.checkVariableType(tbl) !== 'string') {
            throw Error('State Error: triggerAllForTable() needs string tbl-code');
        }

        if ($A.generic.checkVariableType(container) !== 'domelement') {
            container = document;
        }

        components = $A.dom.searchAllElementsCorrectly('[data-state-initialize]', container);
        components.forEach((component) => {
            $A.ux.triggerSingleForTable(tbl, component);
        });
    },

    triggerSingleForTable: function(tbl, component) {
        if ($A.generic.checkVariableType(tbl) !== 'string') {
            throw Error('State Error: triggerSingleForTable() needs string tbl-code');
        }
        if ($A.generic.checkVariableType(component) !== 'domelement') {
            throw Error('DOM Error: triggerSingleForTable() needs HTMLElement as component');
        }

        stateAttrs = $A.dom.filterAtrributes(component, 'data-state', null);
        const componentId = component.id;
        const triggerKey = null;
        const initialize = false;
        let mapper = {};
        app = $A.dom.searchElementCorrectly('[data-state-app-name]').dataset.stateAppName;

        if ($A.generic.checkVariableType(app) !== 'string' || $A.generic.isVariableEmpty(app)) {
            throw Error('State Error: App name could not be found.');
        }

        stateAttrs.forEach((attr) => {
            if (attr[0] === 'data-state-initialize') {
                initialize = attr[1];
            }
            if (attr[0] === 'data-state-key') {
                triggerKey = attr[1];
            }
            if (attr[1].startsWith('data-state-mapper')) {
                let parts = attr[0].split('-');
                let key = parts.slice(3).join('-');
                mapper[key] = attr[1];
            }
        });

        if ($A.generic.isVariableEmpty(triggerKey)) {
            triggerKey = componentId;
        }

        $A.state.trigger(triggerKey, mapper);
    }
};

