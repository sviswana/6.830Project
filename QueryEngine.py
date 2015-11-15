from enum import Enum


class QueryEngine:
    def __init__(self, socket):
        pass


    DATA_SEPARATOR = "|"
    QTYPE_SEPARATOR = "#"
    QUERY_SEPARATOR = ";"

    def serialize(self, query):
        if not query:
            raise QueryError("No data provided for query");
        qType, dateTime, keyword = query[0], query[1], query[2]

        serString = DATA_SEPARATOR.join(data[1:end]);

        serString =  QTYPE_SEPARATOR.join([qType.value, serString])
        return serString;

    def deserialize(self, query):
        if not query:
            raise QueryError("No data provided for query");
        qtype_val, data = query.split(QTYPE_SEPARATOR);
        qtype = int(qtype_val);
        return [qtype].append(data.split(DATA_SEPARATOR));

class QueryType(Enum):
    UPDATE = 1
    INSERT = 2
    SELECT = 3

class QueryError(Exception):
     def __init__(self, value):
         self.value = value

     def __str__(self):
         return repr(self.value)
