import pytest
from monarch_py.implementations.solr.solr_implementation import SolrImplementation


def test_entity():
    si = SolrImplementation()
    entity = si.get_entity("MONDO:0007947")
    assert entity
    assert entity.name == "Marfan syndrome"

@pytest.mark.parametrize(
    "query", [
        "fgf8a",
        "MONDO:0015938",
        # TODO: we need improved tokenization in the solr-schema before indexing so that
        #  multi-word queries will work
        # "Alzheimer disease 16",
        # "breast cancer"
        # "AD16",
        # "symphalangism, C. S. Lewis type"
    ]
)
def test_search_query_has_some_results(query: str):
    si = SolrImplementation()
    response = si.search(query)
    assert response
    assert response.total > 0
