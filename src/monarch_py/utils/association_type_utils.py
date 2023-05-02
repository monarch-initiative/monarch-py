import pkgutil
from typing import List, Tuple

import yaml
from pydantic import parse_obj_as

from monarch_py.datamodels.model import AssociationTypeMapping, AssociationTypeEnum


class AssociationTypeMappings:
    __instance = None

    def __init__(self):
        if AssociationTypeMappings.__instance is not None:
            raise Exception(
                "AssociationTypeMappings is a singleton class, use getInstance() to get the instance."
            )
        else:
            AssociationTypeMappings.__instance = self
            self.mappings = None
            self.load_mappings()

    @staticmethod
    def mappings():
        if AssociationTypeMappings.__instance is None:
            AssociationTypeMappings()
        return AssociationTypeMappings.__instance.mappings

    def mapping(self, association_type: AssociationTypeEnum):
        for mapping in self.mappings():
            if mapping.type == association_type:
                return mapping

    def load_mappings(self):
        mapping_data = pkgutil.get_data(
            __package__, "../association_type_mappings.yaml"
        )
        mapping_data = yaml.load(mapping_data, Loader=yaml.FullLoader)
        self.mappings = parse_obj_as(List[AssociationTypeMapping], mapping_data)


def get_association_type_mapping_by_query_string(query_string: str) -> AssociationTypeMapping:
    """
    Get the association type mapping for a given query string, splitting the category and predicate components apart
    Args:
        query_string: A solr query string to parse apart for category and predicate

    Returns: An AssociationTypeMapping instance appropriate for the given query string
    Raises: ValueError if no match is found
    """

    category, predicate = _parse_association_type_query_string(query_string)

    # TODO: handle lists of categories and predicates
    matching_types = [
        type
        for type in AssociationTypeMappings.mappings()
        if type.category == category and type.predicate == predicate
    ]

    if len(matching_types) == 0:
        raise ValueError(
            f"No matching association type found for query string: [{query_string}]"
        )
    elif len(matching_types) > 1:
        raise ValueError(
            f"Too many association types found for query string: [{query_string}]"
        )
    else:
        return matching_types[0]

def get_solr_query_fragment(agm: AssociationTypeMapping) -> str:

    query_string = ""
    if len(agm.category) == 1:
        query_string = query_string + f'category:"{agm.category[0]}"'
    elif len(agm.category) > 1:
        query_string = (
            query_string + "("
            " OR ".join([f'category:"{cat}"' for cat in agm.category]) + ")"
        )

    if len(agm.category) > 0 and len(agm.predicate) > 0:
        query_string = query_string + " AND "

    if len(agm.predicate) == 1:
        query_string = query_string + f'predicate:"{agm.predicate[0]}"'
    elif len(agm.predicate) > 1:
        query_string = (
            query_string
            + "("
            + " OR ".join([f'predicate:"{pred}"' for pred in agm.predicate])
            + ")"
        )

    return query_string


def get_sql_query_fragment(agm: AssociationTypeMapping) -> str:
    # Maybe this is too brittle? but why repeat all of that logic for just that tiny difference
    return get_solr_query_fragment(agm).replace(':"', ' = "')


def _parse_association_type_query_string(input_string: str) -> Tuple[str, str]:
    category = None
    predicate = None

    # Split the input string into individual fields
    fields = input_string.split(" AND ")

    for field in fields:
        if "category:" in field:
            try:
                category = ":".join(field.split(":")[-2:]).replace('"', "").strip()
            except:
                raise ValueError('Unable to parse "category" field')
        elif "predicate:" in field:
            try:
                predicate = ":".join(field.split(":")[-2:]).replace('"', "").strip()
            except:
                raise ValueError('Unable to parse "predicate" field')
        else:
            raise ValueError("Input string does not conform to expected format")

    return category, predicate
