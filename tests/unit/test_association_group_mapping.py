import pytest

from monarch_py.datamodels.model import AssociationGroupMapping
from monarch_py.utils.association_group_utils import (
    get_solr_query_fragment,
    get_sql_query_fragment,
)


@pytest.fixture()
def basic_mapping():
    return AssociationGroupMapping(
        association_group_key="gene_phenotype",
        subject_label="Genes",
        object_label="Phenotypes",
        category=["biolink:GeneToPhenotypeAssociation"],
        predicate=["biolink:has_phenotype"],
    )


@pytest.fixture()
def double_predicate_mapping():
    return AssociationGroupMapping(
        association_group_key="correlated_gene",
        subject_label="Genes",
        object_label="Correlated Diseases",
        category=["biolink:GeneToDiseaseAssociation"],
        predicate=["biolink:gene_associated_with_condition", "biolink:contributes_to"],
    )


def test_solr_basic_mapping(basic_mapping):
    query_fragment = get_solr_query_fragment(basic_mapping)
    assert (
        query_fragment
        == 'category:"biolink:GeneToPhenotypeAssociation" AND predicate:"biolink:has_phenotype"'
    )


def test_sql_basic_mapping(basic_mapping):
    query_fragment = get_sql_query_fragment(basic_mapping)
    assert (
        query_fragment
        == 'category = "biolink:GeneToPhenotypeAssociation" AND predicate = "biolink:has_phenotype"'
    )


def test_solr_double_predicate_mapping(double_predicate_mapping):
    query_fragment = get_solr_query_fragment(double_predicate_mapping)
    assert (
        query_fragment
        == 'category:"biolink:GeneToDiseaseAssociation" AND (predicate:"biolink:gene_associated_with_condition" OR predicate:"biolink:contributes_to")'
    )


def test_sql_double_predicate_mapping(double_predicate_mapping):
    query_fragment = get_sql_query_fragment(double_predicate_mapping)
    assert (
        query_fragment
        == 'category = "biolink:GeneToDiseaseAssociation" AND (predicate = "biolink:gene_associated_with_condition" OR predicate = "biolink:contributes_to")'
    )
