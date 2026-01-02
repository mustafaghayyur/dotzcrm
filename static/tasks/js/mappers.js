/**
 * This file will hold various mappers our JS libraries may need to operate with data 
 */

/**
 * taskDetailsMapper works in conjunction with the Fetcher() library
 * @param {object} resultSet - retrieved from Fetcher() internal function fetchResource()
 * @param {string} containerId - html id for the DOM element in which this mapper's rendered HTML would be plugged into
 */
export function taskDetailsMapper(resultSet, containerId) {
    const fields = {
        id: ,
        tid: ,
        did:,
        lid: ,
        sid: ,
        aid: ,
        vid: ,
        description:,
        details:,
        status:,
        visibility: ,
        deadline: ,
        creator_id: ,
        parent_id: ,
        assignor_id: ,
        assignee_id: ,
        dlatest: ,
        llatest: ,
        slatest: ,
        alatest: ,
        vlatest: ,

        tcreate_time: ,
        dcreate_time: ,
        lcreate_time: ,
        screate_time: ,
        acreate_time: ,
        vcreate_time: ,

        tdelete_time: ,
        ddelete_time: ,
        ldelete_time: ,
        sdelete_time: ,
        adelete_time: ,
        vdelete_time: ,

        tupdate_time:,
    }

    // here... can you build be logic that maps the resultSet (with fields matching the 
    // fields const) to a simple two-column table with "Label" and "Value" mapped along side each other...
    
}