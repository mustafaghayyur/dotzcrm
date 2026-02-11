import importlib
from rest_framework.exceptions import ValidationError

from core.lib.state import State
from core.DRMcore.mappers.schema.main import schema
from .crud_o2o import O2OOperations
from .crud_m2m import M2MOperations
from .crud_rlc import RLCOperations

class Operations():
    def __init__(self):
        self.state = State()
        self.mapper = None
        self.state.set('operation', None)
        self.state.set('crudClass', None)
        self.state.set('serializerClass', None)
        self.state.set('dataModel', None)

    def setupEnvironment(self, request, operation):
        if request.data.get('tbl', None) is not None:
            tbl = request.data['tbl']
        else:
            raise ValidationError("Error 800: Missing required 'tbl' parameter to identify model.")
        
        schemaEntry = schema[tbl]
        modelModule = importlib.import_module(schemaEntry['path'])
        Model = getattr(modelModule, schemaEntry['model'])

        serMeta = Model.objects.mapper.serializers(tbl)
        serModule = importlib.import_module(serMeta['path'])

        self.mapper = Model.objects.mapper
        self.state.set('operation', operation)
        self.state.set('crudClass', self.mapper.crudClass(tbl))
        self.state.set('serializerClass', getattr(serModule, serMeta['generic']))
        self.state.set('dataModel', self.mapper.tableTypes(tbl))

        self.state.set('data', request.data)
        self.state.set('user', request.user)

    def initiateOperation(self):
        if self.state.get('dataModel') == 'o2o':
            return O2OOperations(self.state)
        
        if self.state.get('dataModel') == 'm2m':
            return M2MOperations(self.state)
        
        if self.state.get('dataModel') == 'rlc':
            return RLCOperations(self.state)

    def create(self, request):
        self.setupEnvironment(request, 'create')
        return self.initiateOperation().create(request)

    def update(self, request):
        self.setupEnvironment(request, 'update')
        return self.initiateOperation().update(request)

    def delete(self, request):
        """
        @todo: add response message on success
        """
        self.setupEnvironment(request, 'delete')
        return self.initiateOperation().delete(request)

    def read(self, request):
        self.setupEnvironment(request, 'read')
        return self.initiateOperation().read(request)
        
