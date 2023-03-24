import urllib
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from monarch_py.utils.utils import escape


class core(Enum):
    ENTITY = "entity"
    ASSOCIATION = "association"


class HistoPhenoKeys(Enum):
    skeletal_system = "HP:0000924"
    nervous_system = "HP:0000707"
    head_neck = "HP:0000152"
    integument = "HP:0001574"
    eye = "HP:0000478"
    cardiovascular_system = "HP:0001626"
    metabolism_homeostasis = "HP:0001939"
    genitourinary_system = "HP:0000119"
    digestive_system = "HP:0025031"
    neoplasm = "HP:0002664"
    blood = "HP:0001871"
    immune_system = "HP:0002715"
    endocrine = "HP:0000818"
    musculature = "HP:0003011"
    respiratory = "HP:0002086"
    ear = "HP:0000598"
    connective_tissue = "HP:0003549"
    prenatal_or_birth = "HP:0001197"
    growth = "HP:0001507"
    breast = "HP:0000769"


class SolrQuery(BaseModel):
    q: str = "*:*"
    rows: int = 20
    start: int = 1
    facet: bool = True
    facet_min_count = 1
    facet_fields: Optional[List[str]] = Field(default_factory=list)
    facet_queries: Optional[List[str]] = Field(default_factory=list)
    filter_queries: Optional[List[str]] = Field(default_factory=list)
    query_fields: str = None
    def_type: str = "edismax"
    mm: str = "100%"  # All tokens in the query must be found in the doc, equivalent to q.op="AND"
    boost: str = None

    def add_field_filter_query(self, field, value):
        if field is not None and value is not None:
            self.filter_queries.append(f"{field}:{escape(value)}")
        else:
            raise ValueError("Can't add a field filter query without a field and value")
        return self

    def add_filter_query(self, filter_query):
        if filter_query is not None:
            self.filter_queries.append(filter_query)
        else:
            raise ValueError("Can't append an empty filter query")
        return self

    def set_boost(self, boosts: Dict[str, float]):
        """
        Set the boost query parameter, which multiplies the natural score of a document. Each
        key in the dictionary is a query that will be evaluated for each document, and if true,
        the score of the document will be multiplied by the value for that key.

        This method is expected to be used to multiply scores for diseases and human genes primarily,
        but may be worth expanding/refactoring to support data quantity or popularity boosts at some point.

        If that happens, it would make sense to pass additional arguments to this method to further build the
        ranking algorithm.

        Args:
            boosts: dictionary of solr query strings to match against and the multiplier expressed as a float

        Returns:
            self to match builder pattern

        """
        self.boost = "product(" + ",".join([f"if({k},{v},1)" for k, v in boosts.items()]) + ")"
        return self

    def query_string(self):
        return urllib.parse.urlencode(
            {
                self._solrize(k): self._solrize(v)
                for k, v in self.dict().items()
                if v is not None
            },
            doseq=True,
        )

    def _solrize(self, value):
        """
        Rename fields and values as necessary to go from the python API to solr query syntax
        """
        if value == "facet_fields":
            return "facet.field"
        elif value == "facet_queries":
            return "facet.query"
        elif value == "filter_queries":
            return "fq"
        elif value == "query_fields":
            return "qf"
        elif value == "def_type":
            return "defType"
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
    facet_queries: Optional[Dict]


class SolrQueryResult(BaseModel):
    responseHeader: SolrQueryResponseHeader
    response: SolrQueryResponse
    facet_counts: Optional[SolrFacetCounts]
