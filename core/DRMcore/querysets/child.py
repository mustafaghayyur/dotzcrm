from django.db import models
from . import background

from core.helpers import misc

"""
    =======================================================================
    Children QuerySets will be based on the various data-models we use
    in DotzCRM...
    =====================================================================
"""

class CTQuerySet(background.QuerySetManager):
    """
        Primarily for One-to-One types

        One-to-One data models have a singular, unique relation to each other.
        These tables also carry revisions, making the 'latest' demarcation 
        necessary.

        Though this class carries some common functions needed by all 
        child tables of Master Table (M2M, RLC).
    """

    # These are to be set in inherited class:
    tbl = None  # Your table for this QuerySet
    master_col = None  # The foreign key of master table (i.e. Tasks)

    def __init__(self, model=None, query=None, using=None, hints=None):
        self.master_col = self.mapper.master('foreignKeyName')

        super().__init__(model, query, using, hints)

    def fetchById(self, cId):
        """
            Fetch specific CT record by its own ID.
            Applies to O2O, M2M, M2M and RLC Records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE id = %s;
            """

        misc.log(self.master_col, 'Het MG, I doubt you will find this. But if so, we have attempted to test self.master_col here.')
        return self.raw(query, [cId])

    def fetchLatest(self, mtId):
        """
            Fetch the latest of child table record for MT ID.
            One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                AND latest = %s
                ORDER BY create_time DESC
                LIMIT 1;
            """

        latest = self.mapper.values.latest('latest')
        return self.raw(query, [mtId, latest])

    def fetchRevision(self, mtId, revision = 0):
        """
            Fetch a specific revision # of child table record for MT ID.
            When dealing with revisions we try not to fetch by IDs. This is
            wasteful spending.
            We instead refer to revisions by their chronological place (in
            reverse). So index[0] will be the current record. Then index[1]
            will be the last revision before the current one. And so forth.
            
            For One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        return self.raw(query, [mtId, revision])

    def fetchAllRevisionsByMasterId(self, mtId):
        """
            Fetch all revisions of child table record for MT ID.
            One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [mtId])  # returns the whole rawqueryset

    

class RLCQuerySet(CTQuerySet):
    """
        Revision-less Children (RLC) data models. 

        These have no revisions, thus no 'latest' field. However, 
        they too carry a many-to-many relationship with the MT.
    """
    def fetchAllByMasterIdRLC(self, mtId):
        """
            Revision Less children records don't have the 'latest' columns.
            I.e. they don't have revisions.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [mtId])

class M2MQuerySet(CTQuerySet):
    """
        Many-to-Many data models. 

        These also carry revisions. Typically the MT is the First-Table-Id, 
        and a outside-entity is the Second-Table-Id.

        First and Second cols defined in space's Mappers
    """

    def __init__(self, model=None, query=None, using=None, hints=None):
        tbl = self.mappers.getAbbreviationForTable(self.tbl)
        cols = self.mappers.m2mFields(tbl)

        if cols is None:
            raise Exception('Unable to fetch M2M Fields. Abort.')
            
        self.firstColumn = cols['firstCol']
        self.secondColumn = cols['secondCol']
        
        super().__init__(model, query, using, hints)

    def fetchAllCurrentBySecondId(self, secondId):
        """
            Fetch all the latest of child table records referencing secondId.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.secondColumn} = %s
                AND latest = %s
            """

        latest = self.mapper.values.latest('latest')
        return self.raw(query, [secondId, latest])
    
    def fetchAllCurrentByFirstId(self, firstId):
        """
            Fetch all the latest of child table records referencing firstId.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND latest = %s
            """

        latest = self.mapper.values.latest('latest')
        return self.raw(query, [firstId, latest])

    def fetchAllRevisions(self, firstId, secondId):
        """
            Fetch revision history of CT records for First & Second Ids.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND {self.secondColumn} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [firstId, secondId])

    def fetchRevision(self, firstId, secondId, revision = 0):
        """
            Fetch a specific revision # (zero-indexed) of child table record 
            for One Id.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND {self.secondColumn} = %s
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        return self.raw(query, [firstId, secondId, revision])
