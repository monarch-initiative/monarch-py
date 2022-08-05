from pydantic import BaseModel
from typing import List, Any


class SolrQuery(BaseModel):
    q: str = "*:*"
    rows: int
    start: int
    filterQueries: List[str]


class SolrQueryResponseHeader(BaseModel):
    Qtime: int
    params: Any


class SolrQueryResponse(BaseModel):
    numFound: int
    start: int
    docs: List[Any]


class SolrQueryResult(BaseModel):
    responseHeader: SolrQueryResponseHeader
    response: SolrQueryResponse
