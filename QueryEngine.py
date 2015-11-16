from enum import Enum


class QueryEngine:
    def __init__(self):
        pass


    DATA_SEPARATOR = "|"
    QTYPE_SEPARATOR = "#"
    QUERY_SEPARATOR = ";"

    def serialize(self, query):
        if not query:
            raise QueryError("No data provided for query");
        qType, dateTime, keyword = query[0], query[1], query[2]

        serString = self.DATA_SEPARATOR.join(str(val) for val in query[1:]);

        serString =  self.QTYPE_SEPARATOR.join(str(val) for val in [qType.value, serString])
        return serString + self.QUERY_SEPARATOR;

    def deserialize(self, fullquery):
        if not fullquery:
            raise QueryError("No data provided for query");
        query = fullquery.split(self.QUERY_SEPARATOR)[0]
        qtype_val, data = query.split(self.QTYPE_SEPARATOR);
        qtype = QueryType(int(qtype_val));


        extractedQuery = data.split(self.DATA_SEPARATOR)
        for index in xrange(0, len(list(extractedQuery))):
            try:
                int_val = int(extractedQuery[index])
                extractedQuery[index] = int_val
            except ValueError:
                continue
        extractedQuery.insert(0, qtype)
        return extractedQuery

class QueryType(Enum):
    UPDATE = 1
    INSERT = 2
    SELECT = 3

class QueryError(Exception):
     def __init__(self, value):
         self.value = value

     def __str__(self):
         return repr(self.value)

if __name__ =='__main__':
    qe = QueryEngine()
    qt = QueryType.UPDATE
    timestamp = "time"
    keyword = "keyword"
    count = 1
    query = [qt, timestamp, keyword, count]
    serialExpected = str(QueryType.UPDATE.value) + qe.QTYPE_SEPARATOR + timestamp + qe.DATA_SEPARATOR + keyword + qe.DATA_SEPARATOR + str(count) + qe.QUERY_SEPARATOR
    serialProduced = qe.serialize(query)
    if not (serialExpected == serialProduced):
        raise QueryError("Error in format of query")

    print qe.deserialize(serialExpected)
    print query