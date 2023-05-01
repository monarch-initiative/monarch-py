import pkgutil
from typing import List, Tuple

import yaml
from pydantic import parse_obj_as

from monarch_py.datamodels.model import AssociationGroupMapping


class AssociationGroupMappings:
    __instance = None

    def __init__(self):
        if AssociationGroupMappings.__instance is not None:
            raise Exception(
                "AssociationGroupMappings is a singleton class, use getInstance() to get the instance."
            )
        else:
            AssociationGroupMappings.__instance = self
            self.mappings = None
            self.load_mappings()

    @staticmethod
    def mappings():
        if AssociationGroupMappings.__instance is None:
            AssociationGroupMappings()
        return AssociationGroupMappings.__instance.mappings

    def load_mappings(self):
        mapping_data = pkgutil.get_data(
            __package__, "../association_group_mappings.yaml"
        )
        mapping_data = yaml.load(mapping_data, Loader=yaml.FullLoader)
        self.mappings = parse_obj_as(List[AssociationGroupMapping], mapping_data)


def get_association_group_mapping(query_string: str) -> AssociationGroupMapping:
    """
    Get the association group mapping for a given query string, splitting the category and predicate components apart
    Args:
        query_string: A solr query string to parse apart for category and predicate

    Returns: An AssociationGroupMapping instance appropriate for the given query string
    Raises: ValueError if no match is found
    """

    category, predicate = _parse_association_group_query_string(query_string)

    matching_groups = [
        group
        for group in AssociationGroupMappings.mappings()
        if group.category == category and group.predicate == predicate
    ]

    if len(matching_groups) == 0:
        raise ValueError(
            f"No matching association group found for query string: [{query_string}]"
        )
    elif len(matching_groups) > 1:
        raise ValueError(
            f"Too many association groups found for query string: [{query_string}]"
        )
    else:
        return matching_groups[0]


def get_solr_query_fragment(agm: AssociationGroupMapping) -> str:
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


def get_sql_query_fragment(agm: AssociationGroupMapping) -> str:
    # Maybe this is too brittle? but why repeat all of that logic for just that tiny difference
    return get_solr_query_fragment(agm).replace(':"', ' = "')


def _parse_association_group_query_string(input_string: str) -> Tuple[str, str]:
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
