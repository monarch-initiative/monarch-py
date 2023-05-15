from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


class AssociationDirectionEnum(str, Enum):

    incoming = "incoming"
    outgoing = "outgoing"


class AssociationTypeEnum(str, Enum):

    disease_phenotype = "disease_phenotype"
    gene_phenotype = "gene_phenotype"
    gene_interaction = "gene_interaction"
    gene_pathway = "gene_pathway"
    gene_expression = "gene_expression"
    gene_orthology = "gene_orthology"
    chemical_pathway = "chemical_pathway"
    gene_function = "gene_function"
    correlated_gene = "correlated_gene"
    causal_gene = "causal_gene"


class Association(ConfiguredBaseModel):

    aggregator_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(None)
    subject: str = Field(None)
    original_subject: Optional[str] = Field(None)
    subject_namespace: Optional[str] = Field(None)
    subject_category: Optional[List[str]] = Field(default_factory=list)
    subject_closure: Optional[List[str]] = Field(default_factory=list)
    subject_label: Optional[str] = Field(None)
    subject_closure_label: Optional[List[str]] = Field(default_factory=list)
    predicate: str = Field(None)
    object: str = Field(None)
    original_object: Optional[str] = Field(None)
    object_namespace: Optional[str] = Field(None)
    object_category: Optional[List[str]] = Field(default_factory=list)
    object_closure: Optional[List[str]] = Field(default_factory=list)
    object_label: Optional[str] = Field(None)
    object_closure_label: Optional[List[str]] = Field(default_factory=list)
    primary_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    category: Optional[List[str]] = Field(default_factory=list)
    negated: Optional[bool] = Field(None)
    provided_by: Optional[str] = Field(None)
    publications: Optional[List[str]] = Field(default_factory=list)
    qualifiers: Optional[List[str]] = Field(default_factory=list)
    frequency_qualifier: Optional[str] = Field(None)
    has_evidence: Optional[str] = Field(None)
    onset_qualifier: Optional[str] = Field(None)
    sex_qualifier: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    stage_qualifier: Optional[str] = Field(None)
    pathway: Optional[str] = Field(None)
    relation: Optional[str] = Field(None)


class DirectionalAssociation(Association):
    """
    An association that gives it's direction relative to a specified entity
    """

    direction: AssociationDirectionEnum = Field(
        None,
        description="""The directionality of the association relative to a given entity for an association_count. If the entity is the subject or in the subject closure, the direction is forwards, if it is the object or in the object closure, the direction is backwards.""",
    )
    aggregator_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(None)
    subject: str = Field(None)
    original_subject: Optional[str] = Field(None)
    subject_namespace: Optional[str] = Field(None)
    subject_category: Optional[List[str]] = Field(default_factory=list)
    subject_closure: Optional[List[str]] = Field(default_factory=list)
    subject_label: Optional[str] = Field(None)
    subject_closure_label: Optional[List[str]] = Field(default_factory=list)
    predicate: str = Field(None)
    object: str = Field(None)
    original_object: Optional[str] = Field(None)
    object_namespace: Optional[str] = Field(None)
    object_category: Optional[List[str]] = Field(default_factory=list)
    object_closure: Optional[List[str]] = Field(default_factory=list)
    object_label: Optional[str] = Field(None)
    object_closure_label: Optional[List[str]] = Field(default_factory=list)
    primary_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    category: Optional[List[str]] = Field(default_factory=list)
    negated: Optional[bool] = Field(None)
    provided_by: Optional[str] = Field(None)
    publications: Optional[List[str]] = Field(default_factory=list)
    qualifiers: Optional[List[str]] = Field(default_factory=list)
    frequency_qualifier: Optional[str] = Field(None)
    has_evidence: Optional[str] = Field(None)
    onset_qualifier: Optional[str] = Field(None)
    sex_qualifier: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    stage_qualifier: Optional[str] = Field(None)
    pathway: Optional[str] = Field(None)
    relation: Optional[str] = Field(None)


class Entity(ConfiguredBaseModel):

    id: str = Field(None)
    category: Optional[List[str]] = Field(default_factory=list)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    in_taxon: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    symbol: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)


class HistoPheno(ConfiguredBaseModel):

    id: str = Field(None)
    items: List[HistoBin] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )


class Results(ConfiguredBaseModel):

    limit: int = Field(None, description="""number of items to return in a response""")
    offset: int = Field(None, description="""offset into the total number of items""")
    total: int = Field(None, description="""total number of items matching a query""")


class AssociationResults(Results):

    items: List[Association] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(None, description="""number of items to return in a response""")
    offset: int = Field(None, description="""offset into the total number of items""")
    total: int = Field(None, description="""total number of items matching a query""")


class AssociationTableResults(Results):

    items: List[DirectionalAssociation] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(None, description="""number of items to return in a response""")
    offset: int = Field(None, description="""offset into the total number of items""")
    total: int = Field(None, description="""total number of items matching a query""")


class EntityResults(Results):

    items: List[Entity] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(None, description="""number of items to return in a response""")
    offset: int = Field(None, description="""offset into the total number of items""")
    total: int = Field(None, description="""total number of items matching a query""")


class SearchResult(Entity):

    highlight: Optional[str] = Field(
        None, description="""matching text snippet containing html tags"""
    )
    score: Optional[float] = Field(None)
    id: str = Field(None)
    category: List[str] = Field(default_factory=list)
    name: str = Field(None)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    in_taxon: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    symbol: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)


class SearchResults(Results):

    items: List[SearchResult] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    facet_fields: Optional[Dict[str, FacetField]] = Field(
        default_factory=dict,
        description="""Collection of facet field responses with the field values and counts""",
    )
    facet_queries: Optional[Dict[str, FacetValue]] = Field(
        default_factory=dict,
        description="""Collection of facet query responses with the query string values and counts""",
    )
    limit: int = Field(None, description="""number of items to return in a response""")
    offset: int = Field(None, description="""offset into the total number of items""")
    total: int = Field(None, description="""total number of items matching a query""")


class FacetValue(ConfiguredBaseModel):

    label: str = Field(None)
    count: Optional[int] = Field(None, description="""count of documents""")


class HistoBin(FacetValue):

    id: str = Field(None)
    label: str = Field(None)
    count: Optional[int] = Field(None, description="""count of documents""")


class FacetField(ConfiguredBaseModel):

    label: str = Field(None)
    facet_values: Optional[Dict[str, FacetValue]] = Field(default_factory=dict)


class AssociationTypeMapping(ConfiguredBaseModel):
    """
    A data class to hold the necessary information to produce association type counts for given  entities with appropriate directional labels
    """

    association_type: Optional[AssociationTypeEnum] = Field(None)
    subject_label: Optional[str] = Field(
        None,
        description="""A label to describe the subjects of the association type as a whole for use in the UI""",
    )
    object_label: Optional[str] = Field(
        None,
        description="""A label to describe the objects of the association type as a whole for use in the UI""",
    )
    symmetric: bool = Field(
        False,
        description="""Whether the association type is symmetric, meaning that the subject and object labels should be interchangeable""",
    )
    category: Optional[List[str]] = Field(
        default_factory=list,
        description="""The biolink categories to use in queries for this association type, assuming OR semantics""",
    )
    predicate: List[str] = Field(
        default_factory=list,
        description="""The biolink predicate to use in queries for this association type, assuming OR semantics""",
    )


class AssociationCount(FacetValue):

    association_type: Optional[AssociationTypeEnum] = Field(None)
    label: str = Field(None)
    count: Optional[int] = Field(None, description="""count of documents""")


class AssociationCountList(ConfiguredBaseModel):
    """
    Container class for a list of association counts
    """

    items: List[AssociationCount] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Association.update_forward_refs()
DirectionalAssociation.update_forward_refs()
Entity.update_forward_refs()
HistoPheno.update_forward_refs()
Results.update_forward_refs()
AssociationResults.update_forward_refs()
AssociationTableResults.update_forward_refs()
EntityResults.update_forward_refs()
SearchResult.update_forward_refs()
SearchResults.update_forward_refs()
FacetValue.update_forward_refs()
HistoBin.update_forward_refs()
FacetField.update_forward_refs()
AssociationTypeMapping.update_forward_refs()
AssociationCount.update_forward_refs()
AssociationCountList.update_forward_refs()
