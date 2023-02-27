import pytest
from monarch_py.implementations.solr.solr_implementation import SolrImplementation


@pytest.mark.parametrize(
    "query", [
        "fgf8a",
        "MONDO:0015938",
        "Alzheimer disease 16",
        "breast cancer",
# Failing because we don't have synonyms coming in from Phenio (!)
#        "AD16",
        "symphalangism, C. S. Lewis type"
    ]
)
def test_search_query_has_some_results(query: str):
    si = SolrImplementation()
    response = si.search(query)
    assert response
    assert response.total > 0

def test_facet_fields():
    si = SolrImplementation()
    response = si.search("syndrome", facet_fields=["category", "taxon"])
    assert response
    assert response.total > 0
    assert response.facets
    assert response.facets["category"]

def test_facet_queries():
    si = SolrImplementation()
    response = si.search("syndrome", facet_queries=["object_closure:\"HP:0000924\"", "object_closure:\"HP:0000119\""])
    assert response
    assert response.total > 0
    assert response.facet_queries["object_closure:\"HP:0000924\""] > 10
    assert response.facet_queries["object_closure:\"HP:0000119\""] > 10
