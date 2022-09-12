import json
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
        return entity

    def query(self, q: SolrQuery) -> SolrQueryResult:
        url = f"{self.base_url}/{self.core.value}/select?{q.query_string()}"
        response = requests.get(url)
        data = json.loads(response.text)
        return SolrQueryResult.parse_obj(data)

    def _strip_json(self, doc: dict, *fields_to_remove: str):
        for field in fields_to_remove:
            try:
                del doc[field]
            except KeyError:
                pass
        return doc


