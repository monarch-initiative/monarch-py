from __future__ import annotations

import sys
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import Field

if sys.version_info >= (3, 8):
    pass
else:
    pass


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
    use_enum_values=True,
):
    pass


class AssociationDirectionEnum(str, Enum):
    """
    The directionality of an association as it relates to a specified entity, with edges being categorized as incoming or outgoing
    """

    # An association for which a specified entity is the object or part of the object closure
    incoming = "incoming"
    # An association for which a specified entity is the subject or part of the subject closure
    outgoing = "outgoing"


class Association(ConfiguredBaseModel):

    aggregator_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    subject: str = Field(...)
    original_subject: Optional[str] = Field(None)
    subject_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the subject entity"""
    )
    subject_category: Optional[str] = Field(
        None, description="""The category of the subject entity"""
    )
    subject_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing subject id and the ids of all of it's ancestors""",
    )
    subject_label: Optional[str] = Field(
        None, description="""The name of the subject entity"""
    )
    subject_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing subject name and the names of all of it's ancestors""",
    )
    predicate: str = Field(...)
    object: str = Field(...)
    original_object: Optional[str] = Field(None)
    object_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the object entity"""
    )
    object_category: Optional[str] = Field(
        None, description="""The category of the object entity"""
    )
    object_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing object id and the ids of all of it's ancestors""",
    )
    object_label: Optional[str] = Field(
        None, description="""The name of the object entity"""
    )
    object_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing object name and the names of all of it's ancestors""",
    )
    primary_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    category: Optional[str] = Field(None)
    negated: Optional[bool] = Field(None)
    provided_by: Optional[str] = Field(None)
    publications: Optional[List[str]] = Field(default_factory=list)
    qualifiers: Optional[List[str]] = Field(default_factory=list)
    frequency_qualifier: Optional[str] = Field(None)
    has_evidence: Optional[str] = Field(None)
    onset_qualifier: Optional[str] = Field(None)
    sex_qualifier: Optional[str] = Field(None)
    stage_qualifier: Optional[str] = Field(None)
    pathway: Optional[str] = Field(None)
    relation: Optional[str] = Field(None)
    frequency_qualifier_label: Optional[str] = Field(
        None, description="""The name of the frequency_qualifier entity"""
    )
    frequency_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the frequency_qualifier entity"""
    )
    frequency_qualifier_category: Optional[str] = Field(
        None, description="""The category of the frequency_qualifier entity"""
    )
    frequency_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing frequency_qualifier id and the ids of all of it's ancestors""",
    )
    frequency_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing frequency_qualifier name and the names of all of it's ancestors""",
    )
    onset_qualifier_label: Optional[str] = Field(
        None, description="""The name of the onset_qualifier entity"""
    )
    onset_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the onset_qualifier entity"""
    )
    onset_qualifier_category: Optional[str] = Field(
        None, description="""The category of the onset_qualifier entity"""
    )
    onset_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing onset_qualifier id and the ids of all of it's ancestors""",
    )
    onset_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing onset_qualifier name and the names of all of it's ancestors""",
    )
    sex_qualifier_label: Optional[str] = Field(
        None, description="""The name of the sex_qualifier entity"""
    )
    sex_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the sex_qualifier entity"""
    )
    sex_qualifier_category: Optional[str] = Field(
        None, description="""The category of the sex_qualifier entity"""
    )
    sex_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing sex_qualifier id and the ids of all of it's ancestors""",
    )
    sex_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing sex_qualifier name and the names of all of it's ancestors""",
    )
    stage_qualifier_label: Optional[str] = Field(
        None, description="""The name of the stage_qualifier entity"""
    )
    stage_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the stage_qualifier entity"""
    )
    stage_qualifier_category: Optional[str] = Field(
        None, description="""The category of the stage_qualifier entity"""
    )
    stage_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing stage_qualifier id and the ids of all of it's ancestors""",
    )
    stage_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing stage_qualifier name and the names of all of it's ancestors""",
    )


class AssociationCountList(ConfiguredBaseModel):
    """
    Container class for a list of association counts
    """

    items: List[AssociationCount] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )


class AssociationTypeMapping(ConfiguredBaseModel):
    """
    A data class to hold the necessary information to produce association type counts for given  entities with appropriate directional labels
    """

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
    category: str = Field(
        ...,
        description="""The biolink category to use in queries for this association type""",
    )


class DirectionalAssociation(Association):
    """
    An association that gives it's direction relative to a specified entity
    """

    direction: AssociationDirectionEnum = Field(
        ...,
        description="""The directionality of the association relative to a given entity for an association_count. If the entity is the subject or in the subject closure, the direction is forwards, if it is the object or in the object closure, the direction is backwards.""",
    )
    aggregator_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    subject: str = Field(...)
    original_subject: Optional[str] = Field(None)
    subject_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the subject entity"""
    )
    subject_category: Optional[str] = Field(
        None, description="""The category of the subject entity"""
    )
    subject_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing subject id and the ids of all of it's ancestors""",
    )
    subject_label: Optional[str] = Field(
        None, description="""The name of the subject entity"""
    )
    subject_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing subject name and the names of all of it's ancestors""",
    )
    predicate: str = Field(...)
    object: str = Field(...)
    original_object: Optional[str] = Field(None)
    object_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the object entity"""
    )
    object_category: Optional[str] = Field(
        None, description="""The category of the object entity"""
    )
    object_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing object id and the ids of all of it's ancestors""",
    )
    object_label: Optional[str] = Field(
        None, description="""The name of the object entity"""
    )
    object_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing object name and the names of all of it's ancestors""",
    )
    primary_knowledge_source: Optional[List[str]] = Field(default_factory=list)
    category: Optional[str] = Field(None)
    negated: Optional[bool] = Field(None)
    provided_by: Optional[str] = Field(None)
    publications: Optional[List[str]] = Field(default_factory=list)
    qualifiers: Optional[List[str]] = Field(default_factory=list)
    frequency_qualifier: Optional[str] = Field(None)
    has_evidence: Optional[str] = Field(None)
    onset_qualifier: Optional[str] = Field(None)
    sex_qualifier: Optional[str] = Field(None)
    stage_qualifier: Optional[str] = Field(None)
    pathway: Optional[str] = Field(None)
    relation: Optional[str] = Field(None)
    frequency_qualifier_label: Optional[str] = Field(
        None, description="""The name of the frequency_qualifier entity"""
    )
    frequency_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the frequency_qualifier entity"""
    )
    frequency_qualifier_category: Optional[str] = Field(
        None, description="""The category of the frequency_qualifier entity"""
    )
    frequency_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing frequency_qualifier id and the ids of all of it's ancestors""",
    )
    frequency_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing frequency_qualifier name and the names of all of it's ancestors""",
    )
    onset_qualifier_label: Optional[str] = Field(
        None, description="""The name of the onset_qualifier entity"""
    )
    onset_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the onset_qualifier entity"""
    )
    onset_qualifier_category: Optional[str] = Field(
        None, description="""The category of the onset_qualifier entity"""
    )
    onset_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing onset_qualifier id and the ids of all of it's ancestors""",
    )
    onset_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing onset_qualifier name and the names of all of it's ancestors""",
    )
    sex_qualifier_label: Optional[str] = Field(
        None, description="""The name of the sex_qualifier entity"""
    )
    sex_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the sex_qualifier entity"""
    )
    sex_qualifier_category: Optional[str] = Field(
        None, description="""The category of the sex_qualifier entity"""
    )
    sex_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing sex_qualifier id and the ids of all of it's ancestors""",
    )
    sex_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing sex_qualifier name and the names of all of it's ancestors""",
    )
    stage_qualifier_label: Optional[str] = Field(
        None, description="""The name of the stage_qualifier entity"""
    )
    stage_qualifier_namespace: Optional[str] = Field(
        None, description="""The namespace/prefix of the stage_qualifier entity"""
    )
    stage_qualifier_category: Optional[str] = Field(
        None, description="""The category of the stage_qualifier entity"""
    )
    stage_qualifier_closure: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing stage_qualifier id and the ids of all of it's ancestors""",
    )
    stage_qualifier_closure_label: Optional[List[str]] = Field(
        default_factory=list,
        description="""Field containing stage_qualifier name and the names of all of it's ancestors""",
    )


class Entity(ConfiguredBaseModel):
    """
    Represents an Entity in the Monarch KG data model
    """

    id: str = Field(...)
    category: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    in_taxon: Optional[str] = Field(
        None, description="""The biolink taxon that the entity is in the closure of."""
    )
    in_taxon_label: Optional[str] = Field(
        None,
        description="""The label of the biolink taxon that the entity is in the closure of.""",
    )
    symbol: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)


class FacetValue(ConfiguredBaseModel):

    label: str = Field(...)
    count: Optional[int] = Field(None, description="""count of documents""")


class AssociationCount(FacetValue):

    category: Optional[str] = Field(None)
    label: str = Field(...)
    count: Optional[int] = Field(None, description="""count of documents""")


class FacetField(ConfiguredBaseModel):

    label: str = Field(...)
    facet_values: Optional[List[FacetValue]] = Field(
        default_factory=list,
        description="""Collection of FacetValue label/value instances belonging to a FacetField""",
    )


class HistoPheno(ConfiguredBaseModel):

    id: str = Field(...)
    items: List[HistoBin] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )


class HistoBin(FacetValue):

    id: str = Field(...)
    label: str = Field(...)
    count: Optional[int] = Field(None, description="""count of documents""")


class Node(Entity):
    """
    UI conatiner class extending Entity with additional information
    """

    in_taxon: Optional[str] = Field(
        None, description="""The biolink taxon that the entity is in the closure of."""
    )
    in_taxon_label: Optional[str] = Field(
        None,
        description="""The label of the biolink taxon that the entity is in the closure of.""",
    )
    inheritance: Optional[Entity] = Field(None)
    association_counts: List[AssociationCount] = Field(default_factory=list)
    node_hierarchy: Optional[NodeHierarchy] = Field(None)
    id: str = Field(...)
    category: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    symbol: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)


class NodeHierarchy(ConfiguredBaseModel):

    super_classes: List[Entity] = Field(default_factory=list)
    equivalent_classes: List[Entity] = Field(default_factory=list)
    sub_classes: List[Entity] = Field(default_factory=list)


class Results(ConfiguredBaseModel):

    limit: int = Field(..., description="""number of items to return in a response""")
    offset: int = Field(..., description="""offset into the total number of items""")
    total: int = Field(..., description="""total number of items matching a query""")


class AssociationResults(Results):

    items: List[Association] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(..., description="""number of items to return in a response""")
    offset: int = Field(..., description="""offset into the total number of items""")
    total: int = Field(..., description="""total number of items matching a query""")


class AssociationTableResults(Results):

    items: List[DirectionalAssociation] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(..., description="""number of items to return in a response""")
    offset: int = Field(..., description="""offset into the total number of items""")
    total: int = Field(..., description="""total number of items matching a query""")


class EntityResults(Results):

    items: List[Entity] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    limit: int = Field(..., description="""number of items to return in a response""")
    offset: int = Field(..., description="""offset into the total number of items""")
    total: int = Field(..., description="""total number of items matching a query""")


class SearchResult(Entity):

    highlight: Optional[str] = Field(
        None, description="""matching text snippet containing html tags"""
    )
    score: Optional[float] = Field(None)
    id: str = Field(...)
    category: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    in_taxon: Optional[str] = Field(
        None, description="""The biolink taxon that the entity is in the closure of."""
    )
    in_taxon_label: Optional[str] = Field(
        None,
        description="""The label of the biolink taxon that the entity is in the closure of.""",
    )
    symbol: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)


class SearchResults(Results):

    items: List[SearchResult] = Field(
        default_factory=list,
        description="""A collection of items, with the type to be overriden by slot_usage""",
    )
    facet_fields: Optional[List[FacetField]] = Field(
        default_factory=list,
        description="""Collection of facet field responses with the field values and counts""",
    )
    facet_queries: Optional[List[FacetValue]] = Field(
        default_factory=list,
        description="""Collection of facet query responses with the query string values and counts""",
    )
    limit: int = Field(..., description="""number of items to return in a response""")
    offset: int = Field(..., description="""offset into the total number of items""")
    total: int = Field(..., description="""total number of items matching a query""")


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Association.update_forward_refs()
AssociationCountList.update_forward_refs()
AssociationTypeMapping.update_forward_refs()
DirectionalAssociation.update_forward_refs()
Entity.update_forward_refs()
FacetValue.update_forward_refs()
AssociationCount.update_forward_refs()
FacetField.update_forward_refs()
HistoPheno.update_forward_refs()
HistoBin.update_forward_refs()
Node.update_forward_refs()
NodeHierarchy.update_forward_refs()
Results.update_forward_refs()
AssociationResults.update_forward_refs()
AssociationTableResults.update_forward_refs()
EntityResults.update_forward_refs()
SearchResult.update_forward_refs()
SearchResults.update_forward_refs()
