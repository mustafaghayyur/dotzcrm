from .RelationshipMappers import RelationshipMappers

class M2MJoins():
    """
        During development it was realized we may need to conduct Database operations
        between mappers. Question is how?

        We will atempt to make the most minimal efforts to allow QuerySet operations
        between two mappers.

        CRUD operations should remain unchanged through this M2M utility development.
    """
    matrix = {}

    def addMapper(self, key, mapperObj):
        if isinstance(key, str) and isinstance(mapperObj, RelationshipMappers):
            self.matrix[key] = mapperObj

    def getMappers(self):
        return self.matrix
    
    def setMapper(self, key):
        if key in self.matrix:
            return self.matrix[key]
        return None
    
    def __getattr__(self, name):
        """
            Here we will do magic, and handle all mapper calls to any of the
            handled mappers, and deliver combined results!
        """
        def callMethod(*args, **kwargs):
            mprs = self.getMappers()
            results = {}
            for key, mapper in mprs.items():
                callable = getattr(mapper, name, None)
                results[key] = callable(*args, **kwargs)
            return self.mergeResults(results)
        
        return callMethod

    def mergeResults(self, combinedResults):
        """
            Massive data handling happens in this method.
            
            Merges results from multiple mappers based on data type.
            Handles: lists, dicts, strings, integers, and None values.
            
            Args:
                combinedResults: Dict with mapper results {key: resultset}
                
            Returns:
                Merged result of appropriate type, or None if no valid results
        """
        if not combinedResults:
            return None
        
        mprs = self.getMappers()
        keys = mprs.keys()
        
        # Filter out None values
        valid_results = {k: v for k, v in combinedResults.items() if v is not None}
        
        if not valid_results:
            return None
        
        # Get the first non-None value to determine type
        first_value = next(iter(valid_results.values()))
        
        # Merge based on type
        if isinstance(first_value, list):
            merged = []
            for result in valid_results.values():
                if isinstance(result, list):
                    merged.extend(result)
            return merged
        
        if isinstance(first_value, dict):
            merged = {}
            for result in valid_results.values():
                if isinstance(result, dict):
                    merged.update(result)
            return merged
        
        if isinstance(first_value, str) or isinstance(first_value, int):
            merged = {}
            for key in keys:
                if key in valid_results:
                    merged[key] = valid_results[key]
            return merged
        
        return None
    