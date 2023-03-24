import pytest

from monarch_py.implementations.solr.solr_implementation import SolrImplementation

@pytest.mark.parametrize("q, should_return",
                         [("down syn", "Down syndrome"),
                          ("marf", "Marfan syndrome")])
def test_autocomplete(q, should_return):
    si = SolrImplementation()
    response = si.autocomplete(q)
    assert response
    assert response.total > 0

    names = [x.name for x in response.items]
    names.extend([x.symbol for x in response.items if x.symbol])
    print(names)
    assert should_return in names
