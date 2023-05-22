import pytest

from monarch_py.datamodels.model import AssociationDirectionEnum, AssociationTypeEnum
from monarch_py.implementations.solr.solr_implementation import SolrImplementation

# def check_solr_available():
#     import requests
#     try:
#         response = requests.get("https://monarchinitiative.org/v3/api")
#         return response.status_code == 200
#     except Exception as e:
#         return False
# pytestmark = pytest.mark.skipif(
#     condition = not check_solr_available(),
#     reason = "Solr is not available",
# )

pytestmark = pytest.mark.skip(reason="Solr backend not yet available")


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

def test_search_sort():
    si = SolrImplementation()
    response = si.search("marfan", sort="name desc")
    assert response
    assert response.total > 0
    assert response.items[0].name > response.items[-1].name

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


def test_association_counts_for_disease():
    si = SolrImplementation()
    association_counts = si.get_association_counts(entity="MONDO:0007947")
    assert association_counts
    assert len(association_counts) > 0

    causal_genes = [
        ac for ac in association_counts if ac.association_type == "causal_gene"
    ][0]
    assert causal_genes.label == "Causal Genes"

    disease_phenotype = [
        ac for ac in association_counts if ac.association_type == "disease_phenotype"
    ][0]
    assert disease_phenotype.label == "Phenotypes"


def test_association_counts_for_phenotype():
    si = SolrImplementation()
    association_counts = si.get_association_counts(entity="HP:0000707")  # HP:0025096 ?
    assert association_counts
    assert len(association_counts) > 0

    disease_phenotype = [
        ac for ac in association_counts if ac.association_type == "disease_phenotype"
    ][0]
    assert disease_phenotype.label == "Diseases"

    gene_phenotype = [
        ac for ac in association_counts if ac.association_type == "gene_phenotype"
    ][0]
    assert gene_phenotype.label == "Genes"


def test_association_table():
    si = SolrImplementation()
    association_results = si.get_association_table(
        "MONDO:0007947", AssociationTypeEnum.disease_phenotype
    )
    assert association_results
    assert association_results.total > 5
    assert association_results.items[0].direction == AssociationDirectionEnum.outgoing
