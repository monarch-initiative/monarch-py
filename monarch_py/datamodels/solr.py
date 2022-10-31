import urllib

from pydantic import BaseModel, Field
from typing import List, Any, Optional, Dict
from enum import Enum


class core(Enum):
    ENTITY = "entity"
    ASSOCIATION = "association"


class SolrQuery(BaseModel):
    q: str = "*:*"
    rows: int = 20
    start: int = 1
    facet: bool = False
    facet_min_count = 1
    facet_fields: List[str] = None
    filter_queries: List[str] = None

    def query_string(self):
        return urllib.parse.urlencode({self._solrize(k): self._solrize(v)
                                       for k, v in self.dict().items()
                                       if v is not None}, doseq=True)

    def _solrize(self, value):
        """
        Rename fields and values as necessary to go from the python API to solr query syntax
        """
        if value == "facet_fields":
            return "facet.field"
        elif value == "filter_queries":
            return "fq"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        else:
            return value


class SolrQueryResponseHeader(BaseModel):
    QTime: int
    params: Any


class SolrQueryResponse(BaseModel):
    num_found: int = Field(alias="numFound")
    start: int
    docs: List[Any]


class SolrFacetCounts(BaseModel):
    facet_fields: Optional[Dict]


class SolrQueryResult(BaseModel):
    responseHeader: SolrQueryResponseHeader
    response: SolrQueryResponse
    facet_counts: Optional[SolrFacetCounts]

