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


class Entity(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    category: Optional[List[str]] = Field(default_factory=list)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    xref: Optional[List[str]] = Field(default_factory=list)
    provided_by: Optional[str] = Field(None)
    in_taxon: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    symbol: Optional[str] = Field(None)
    synonyms: Optional[List[str]] = Field(default_factory=list)
    type: Optional[str] = Field(None)
    synonym: Optional[List[str]] = Field(default_factory=list)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Entity.update_forward_refs()

