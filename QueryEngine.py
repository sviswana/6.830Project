class QueryEngine:
    UPDATE = 'update'
    INSERT = 'insert'
    SELECT = 'select'

    def __init__(self, socket):
        self.socket = socket

    def serialize(self, object):
        pass
    def deserialize(self, object):
        pass

class QueryType(Enum):
    UPDATE = 1
    INSERT = 2
    SELECT = 3
