from dataclasses import dataclass
from enum import Enum

from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.search_interface import SearchInterface


class core(Enum):
    ENTITY = "entity"
    ASSOCIATION = "association"


@dataclass
class MonarchSolrImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """
    Wraps the Monarch Solr endpoint
    """

    def _default_url(self):
        return "http://localhost:8983/solr"

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: EntityInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_entity(
        self, id: str, get_association_counts: bool = False, get_hierarchy: bool = False
    ):
        core_url = self._default_url() + f"/{core.ENTITY}"
        url = f"{core_url}/get?id={id}"
        r = requests.get(url)
        entity = r.json()["doc"]
        strip_json(entity, "_version_")

        if get_association_counts:
            association_counts = get_entity_association_counts(id)
            entity["association_counts"] = association_counts

        if get_hierarchy:
            entity["node_hierarchy"] = get_node_hierarchy(id)

        return entity["node_hierarchy"]
        return entity

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: AssociationInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def get_node_hierarchy(entity_id):
    superClasses = f""

    # query_params = {
    #     q: str = "*:*",
    #     offset: int = 0,
    #     limit: int = 20,
    #     category: str = None,
    #     predicate: str = None,
    #     subject: str = None,
    #     object: str = None,
    #     entity: str = None, # return nodes where entity is subject or object
    #     between: str = None
    # }

    query = build_association_query(
        {
            #'q':'*:*',
            "entity": f'"{entity_id}"',
            "predicate": "biolink:same_as",
        }
    )
    equivalentClasses = requests.get(f"{solr_url}/association/select{query}").json()

    subClasses = ""
    return {
        "superClasses": superClasses,
        "equivalentClasses": equivalentClasses,
        "subClasses": subClasses,
    }
