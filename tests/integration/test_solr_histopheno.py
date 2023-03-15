from monarch_py.implementations.solr.solr_implementation import SolrImplementation

def test_histopheno():
    si = SolrImplementation()
    hp = si.get_histopheno("MONDO:0020121")

    total = 0
    for k in hp.items:
        total += k.count
        
    assert hp.items[0].id == "HP:0000924"