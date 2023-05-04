import pytest

from monarch_py.implementations.solr.solr_implementation import SolrImplementation

pytestmark = pytest.mark.skip(reason = "Solr backend not yet available")

def test_entity():
    si = SolrImplementation()
    entity = si.get_entity("MONDO:0007947")
    assert entity
    assert entity.name == "Marfan syndrome"
