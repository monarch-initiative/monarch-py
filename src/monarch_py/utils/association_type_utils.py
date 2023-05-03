import pkgutil
import re
from typing import List, Tuple

import yaml
from pydantic import parse_obj_as

from monarch_py.datamodels.model import AssociationTypeEnum, AssociationTypeMapping


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
    def get_mappings():
        if AssociationTypeMappings.__instance is None:
            AssociationTypeMappings()
        return AssociationTypeMappings.__instance.mappings

    def get_mapping(self, association_type: AssociationTypeEnum):
        for mapping in self.mappings:
            if mapping.association_type == association_type:
                return mapping

    def load_mappings(self):
        mapping_data = pkgutil.get_data(
            __package__, "../association_type_mappings.yaml"
        )
        mapping_data = yaml.load(mapping_data, Loader=yaml.FullLoader)
        self.mappings = parse_obj_as(List[AssociationTypeMapping], mapping_data)


def get_association_type_mapping_by_query_string(
    query_string: str,
) -> AssociationTypeMapping:
    """
    Get the association type mapping for a given query string, splitting the category and predicate components apart
    Args:
        query_string: A solr query string to parse apart for category and predicate

    Returns: An AssociationTypeMapping instance appropriate for the given query string
    Raises: ValueError if no match is found
    """

    categories, predicates = parse_association_type_query_string(query_string)

    matching_types = [
        a_type
        for a_type in AssociationTypeMappings.get_mappings()
        if set(a_type.category) == set(categories)
        and set(a_type.predicate) == set(predicates)
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


def parse_association_type_query_string(
    query_string: str,
) -> Tuple[List[str], List[str]]:
    categories = []
    predicates = []

    pattern = re.compile(r'(category|predicate):\s*"?([\w:]+)"?')
    for match in re.findall(pattern, query_string):
        if match[0] == "category":
            categories.append(match[1])
        elif match[0] == "predicate":
            predicates.append(match[1])

    # Check if both categories and predicates were found
    if not categories and not predicates:
        raise ValueError("No categories or predicates found in query string")

    return categories, predicates
