from monarch_py.implementations.solr.solr_implentation import SolrImplementation


def test_associations():
    si = SolrImplementation()

    result = si.get_associations()
    assert(result)
    assert(result.response.num_found > 100000)
    assert(len(result.response.docs) == 20)


def test_association_page_limit():
    si = SolrImplementation()

    result = si.get_associations(limit=100)
    assert(len(result.response.docs) == 100)


def test_association_page_number():
    si = SolrImplementation()
    result = si.get_associations(page=2, limit=100)
    assert(result.responseHeader.params['start'] == '101')


def test_association_category():
    si = SolrImplementation()
    result = si.get_associations(category='biolink:GeneToDiseaseAssociation')

    assert (result)
    assert (result.response.num_found > 6000)
    assert ('biolink:GeneToDiseaseAssociation' in result.response.docs[0]["category"])


def test_association_predicate():
    si = SolrImplementation()
    result = si.get_associations(predicate='biolink:has_phenotype')

    assert (result)
    assert (result.response.num_found > 600000)
    assert ('biolink:has_phenotype' in result.response.docs[0]["predicate"])


def test_subject():
    si = SolrImplementation()
    result = si.get_associations(subject="MONDO:0007947")
    assert(result)
    assert(result.response.num_found > 50)
    assert(result.response.docs[0]["subject"] == "MONDO:0007947")


def test_object():
    si = SolrImplementation()
    result = si.get_associations(object="MONDO:0007947")
    assert (result)
    assert (result.response.num_found > 1)
    assert (result.response.docs[0]["object"] == "MONDO:0007947")


def test_entity():
    si = SolrImplementation()
    result = si.get_associations(entity="MONDO:0007947")
    assert (result)
    assert (result.response.num_found > 50)
    for doc in result.response.docs:
        assert(doc["subject"] == "MONDO:0007947" or doc["object"] == "MONDO:0007947")


def test_between():
    si = SolrImplementation()
    result = si.get_associations(between="MONDO:0007947,HP:0000098")
    assert (result)
    assert (result.response.num_found > 0)
    for doc in result.response.docs:
        assert(doc["subject"] == "MONDO:0007947" and doc["object"] == "HP:0000098")


def test_between_reversed():
    si = SolrImplementation()
    result = si.get_associations(between="HP:0000098,MONDO:0007947")
    assert (result)
    assert (result.response.num_found > 0)
    for doc in result.response.docs:
        assert(doc["subject"] == "MONDO:0007947" and doc["object"] == "HP:0000098")

