from monarch_py.implementations.solr.solr_implentation import SolrImplementation


def test_associations():
    si = SolrImplementation()

    response = si.get_associations()
    assert response
    assert response.total > 100000
    assert len(response.associations) == 20


def test_association_page_limit():
    si = SolrImplementation()

    response = si.get_associations(limit=100)
    assert len(response.associations) == 100


def test_association_category():
    si = SolrImplementation()
    response = si.get_associations(category="biolink:GeneToDiseaseAssociation")

    assert response
    assert response.total > 6000
    assert "biolink:GeneToDiseaseAssociation" in response.associations[0].category


def test_association_predicate():
    si = SolrImplementation()
    response = si.get_associations(predicate="biolink:has_phenotype")

    assert response
    assert response.total > 600000
    assert "biolink:has_phenotype" in response.associations[0].predicate


def test_subject():
    si = SolrImplementation()
    response = si.get_associations(subject="MONDO:0007947")
    assert response
    assert response.total > 50
    assert response.associations[0].subject == "MONDO:0007947"


def test_object():
    si = SolrImplementation()
    response = si.get_associations(object="MONDO:0007947")
    assert response
    assert response.total > 1
    assert response.associations[0].object == "MONDO:0007947"


def test_entity():
    si = SolrImplementation()
    response = si.get_associations(entity="MONDO:0007947")
    assert response
    assert response.total > 50
    for association in response.associations:
        assert (
            association.subject == "MONDO:0007947"
            or association.object == "MONDO:0007947"
        )


def test_between():
    si = SolrImplementation()
    response = si.get_associations(between="MONDO:0007947,HP:0000098")
    assert response
    assert response.total > 0
    for association in response.associations:
        assert (
            association.subject == "MONDO:0007947"
            and association.object == "HP:0000098"
        )


def test_between_reversed():
    si = SolrImplementation()
    response = si.get_associations(between="HP:0000098,MONDO:0007947")
    assert response
    assert response.total > 0
    for association in response.associations:
        assert (
            association.subject == "MONDO:0007947"
            and association.object == "HP:0000098"
        )
