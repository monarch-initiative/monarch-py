from monarch_py.implementations.solr.solr_implentation import SolrImplementation


def test_entity():
    si = SolrImplementation()
    entity = si.get_entity("MONDO:0007947")
    assert entity
    assert entity['name'] == "Marfan syndrome"


def test_entity_with_association_counts():
    si = SolrImplementation()
    entity = si.get_entity("MONDO:0007947", get_association_counts=True)
    assert entity
    assert entity["association_counts"]

