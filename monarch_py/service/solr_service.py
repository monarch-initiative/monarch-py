from pydantic import BaseModel
import requests

from monarch_py.datamodels.solr import SolrQuery, \
    SolrQueryResult, SolrQueryResponse, SolrQueryResponseHeader, SolrFacetCounts, core


class SolrService(BaseModel):
    base_url: str
    core: core

    def get(self, id):
        core_url = self.base_url + f"/{self.core.value}"
        url = f"{core_url}/get?id={id}"
        r = requests.get(url)
        entity = r.json()["doc"]
        self._strip_json(entity, "_version_")

    def query(self, q: SolrQuery): #-> SolrQueryResponse:
        url = f"{self.base_url}/{self.core.value}/select?{q.query_string()}"
        r = requests.get(url)

        # return self._parse_response(r.json())
        return url

    def _parse_response(self, raw_response) -> SolrQueryResult:

        SolrQueryResponse(numFound=raw_response["response"]["numFound"],
                          start=raw_response["response"]["start"],
                          docs=raw_response["response"]["docs"])

    def _strip_json(self, doc: dict, *fields_to_remove: str):
        for field in fields_to_remove:
            try:
                del doc[field]
            except:
                pass
        return doc


