class QueryEngine:
    UPDATE = 'update'
    INSERT = 'insert'
    SELECT = 'select'

    def __init__(self, socket):
        self.socket = socket

    def parse(self, ):

class QueryType(Enum):
    UPDATE = 1
    INSERT = 2
    SELECT = 3
