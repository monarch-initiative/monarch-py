from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel as BaseModel, Field

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'
    
class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True, 
                validate_all = True, 
                underscore_attrs_are_private = True, 
                extra = 'forbid', 
                arbitrary_types_allowed = True):
    pass                    


class Association(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    subject: Optional[str] = Field(None)
    subject_namespace: Optional[str] = Field(None)
    subject_category: Optional[List[str]] = Field(default_factory=list)
    subject_closure: Optional[List[str]] = Field(default_factory=list)
    subject_label: Optional[str] = Field(None)
    subject_closure_label: Optional[List[str]] = Field(default_factory=list)
    predicate: Optional[str] = Field(None)
    object: Optional[str] = Field(None)
    object_namespace: Optional[str] = Field(None)
    object_category: Optional[List[str]] = Field(default_factory=list)
    object_closure: Optional[List[str]] = Field(default_factory=list)
    object_label: Optional[str] = Field(None)
    object_closure_label: Optional[List[str]] = Field(default_factory=list)
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
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Association.update_forward_refs()

