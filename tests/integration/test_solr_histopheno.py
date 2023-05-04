import pytest

from monarch_py.implementations.solr.solr_implementation import SolrImplementation

pytestmark = pytest.mark.skip(reason = "Solr backend not yet available")

def test_histopheno():
    si = SolrImplementation()
    hp = si.get_histopheno("MONDO:0020121")

    total = 0
    for k in hp.items:
        total += k.count

    assert hp.items[0].id == "HP:0003011"
