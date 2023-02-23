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
