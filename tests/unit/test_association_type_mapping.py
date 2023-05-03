import pytest

from monarch_py.datamodels.model import AssociationTypeMapping
from monarch_py.utils.association_type_utils import (
    get_solr_query_fragment,
    get_sql_query_fragment,
    parse_association_type_query_string,
)


@pytest.fixture()
def basic_mapping():
    return AssociationTypeMapping(
        association_type="gene_phenotype",
        subject_label="Genes",
        object_label="Phenotypes",
        category=["biolink:GeneToPhenotypeAssociation"],
        predicate=["biolink:has_phenotype"],
    )


@pytest.fixture()
def double_predicate_mapping():
    return AssociationTypeMapping(
        association_type="correlated_gene",
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


def test_parse_association_type_query_string_single_category():
    query_string = 'category:"biolink:GeneToPhenotypeAssociation"'
    categories, predicates = parse_association_type_query_string(query_string)
    assert categories == ["biolink:GeneToPhenotypeAssociation"]
    assert predicates == []


def test_parse_association_type_query_string_single_category_and_predicate():
    query_string = 'category:"biolink:GeneToPhenotypeAssociation" AND predicate:"biolink:has_phenotype"'
    categories, predicates = parse_association_type_query_string(query_string)
    assert categories == ["biolink:GeneToPhenotypeAssociation"]
    assert predicates == ["biolink:has_phenotype"]


def test_parse_association_type_query_string_multiple_categories_and_predicates():
    query_string = 'category:"biolink:GeneToDiseaseAssociation" AND (predicate:"biolink:gene_associated_with_condition" OR predicate:"biolink:contributes_to")'
    categories, predicates = parse_association_type_query_string(query_string)
    assert categories == ["biolink:GeneToDiseaseAssociation"]
    assert predicates == [
        "biolink:gene_associated_with_condition",
        "biolink:contributes_to",
    ]


def test_parse_association_type_query_string_multiple_categories_and_predicates_with_or_operator():
    query_string = '(category:"biolink:GeneToPhenotypeAssociation" OR category:"biolink:GeneToDiseaseAssociation") AND (predicate:"biolink:gene_associated_with_condition" OR predicate:"biolink:contributes_to")'
    categories, predicates = parse_association_type_query_string(query_string)
    assert categories == [
        "biolink:GeneToPhenotypeAssociation",
        "biolink:GeneToDiseaseAssociation",
    ]
    assert predicates == [
        "biolink:gene_associated_with_condition",
        "biolink:contributes_to",
    ]
