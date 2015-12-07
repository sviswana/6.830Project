from enum import Enum
import json

class QueryEngine:
    def __init__(self):
        pass


    DATA_SEPARATOR = "|"
    QTYPE_SEPARATOR = "#"
    QUERY_SEPARATOR = ";"

    def serialize(self, query):
        if not query:
            raise QueryError("No data provided for query");
        qType = query[0]

        serString = self.DATA_SEPARATOR.join(str(val) for val in query[1:]);

        serString =  self.QTYPE_SEPARATOR.join(str(val) for val in [qType.value, serString])
        return serString + self.QUERY_SEPARATOR;

    #Do not use
    def serializeJSON(self, query):
        if not query:
            raise QueryError("No data provided for query");
        qType, dateTime, keyword = query[0], query[1], query[2]

        queryDict = {"type": query[0].value, "timestamp": query[1], "keyword" : query[2], "data": query[1:]}

        return json.dumps(queryDict)

    def deserialize(self, fullquery):
        print "fullquery", fullquery
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

    #do not use
    def deserializeJSON(self, fullquery):
        print "fullquery", fullquery
        if not fullquery:
            raise QueryError("No data provided for query");
        queryDict = json.loads(fullquery);
        queryDict["type"] = QueryType(queryDict["type"])
        return queryDict

class QueryType(Enum):
    UPDATE = 1
    INSERT = 2
    SELECT = 3
    SELECTRANGE = 4
    SERVER_REPLY = 5
    INC_AVG = 6
    INC_COUNT = 7


class QueryError(Exception):
     def __init__(self, value):
         self.value = value

     def __str__(self):
         return repr(self.value)

if __name__ =='__main__':
    qe = QueryEngine()
    qt = QueryType.SELECTRANGE
    timestamp1 = 1448051559999
    timestamp2 = 1448081559999
    keyword = "Hillary Clinton"
    count = 1
    query = [qt, timestamp1, timestamp2, keyword]
    # serialExpected = str(QueryType.UPDATE.value) + qe.QTYPE_SEPARATOR + timestamp + qe.DATA_SEPARATOR + keyword + qe.DATA_SEPARATOR + str(count) + qe.QUERY_SEPARATOR
    serialProduced = qe.serialize(query)
    print serialProduced
    # if not (serialExpected == serialProduced):
    #     raise QueryError("Error in format of query")

    q =  qe.deserialize(serialProduced)
    print q