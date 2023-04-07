import pytest

from monarch_py.datamodels.model import AssociationLabel
from monarch_py.implementations.solr.solr_implementation import SolrImplementation


@pytest.mark.parametrize(
    "query",
    [
        "fgf8a",
        "MONDO:0015938",
        "Alzheimer disease 16",
        "breast cancer",
        # Failing because we don't have synonyms coming in from Phenio (!)
        #        "AD16",
        "symphalangism, C. S. Lewis type",
    ],
)
def test_search_query_has_some_results(query: str):
    si = SolrImplementation()
    response = si.search(query)
    assert response
    assert response.total > 0


def test_facet_fields():
    si = SolrImplementation()
    response = si.search("syndrome", facet_fields=["category", "in_taxon"])
    assert response
    assert response.total > 0
    assert response.facet_fields
    assert response.facet_fields["category"]


def test_association_facets():
    si = SolrImplementation()
    response = si.get_association_facets(facet_fields=["category"])
    assert response
    assert response.facet_fields
    assert response.facet_fields["category"]
    assert (
        response.facet_fields["category"]
        .facet_values["biolink:DiseaseToPhenotypicFeatureAssociation"]
        .count
        > 100000
    )


def test_association_facet_query():
    si = SolrImplementation()

    response = si.get_association_facets(
        subject_closure="MONDO:0007947",
        facet_queries=[
            'object_closure:"HP:0000924"',
            'object_closure:"HP:0000707"',
            'object_closure:"HP:0000152"',
            'object_closure:"HP:0001574"',
            'object_closure:"HP:0000478"',
        ],
    )
    assert response
    assert response.facet_queries
    assert response.facet_queries['object_closure:"HP:0000924"'].count > 20
    assert response.facet_queries['object_closure:"HP:0000707"'].count > 5
    assert response.facet_queries['object_closure:"HP:0000152"'].count > 20

def test_association_counts():
    si = SolrImplementation()
    response = si.get_association_counts(entity="MONDO:0007947")
    assert response
    assert len(response) > 1

def test_associations_by_label():
    si = SolrImplementation()
    response = si.get_associations(entity="MONDO:0007947", association_label=AssociationLabel.disease_phenotype)

    assert response
    assert response.total > 60
    assert response.items[0].subject == "MONDO:0007947"

