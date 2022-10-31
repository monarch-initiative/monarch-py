import collections
from dataclasses import dataclass
import requests

from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.utilities.utils import strip_json
from monarch_py.datamodels.solr import core, SolrQuery
from monarch_py.service.solr_service import SolrService

@dataclass
class SolrImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """
    Wraps the Monarch Solr endpoint
    """

    default_url: str = "http://localhost:8983/solr"

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: EntityInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_entity(
        self, id: str, get_association_counts: bool = False, get_hierarchy: bool = False
    ):

        solr = SolrService(base_url=self.default_url, core=core.ENTITY)
        entity = solr.get(id)

        if get_association_counts:
            entity["association_counts"] = self.get_entity_association_counts(id)

#        if get_hierarchy:
#            entity["node_hierarchy"] = self.get_node_hierarchy(id)

        return entity


    def get_entity_association_counts(self, id: str):

        solr = SolrService(base_url=self.default_url, core=core.ASSOCIATION)

        object_categories = solr.get_filtered_facet(
            id, filter_field="subject", facet_field="object_category"
        )
        subject_categories = solr.get_filtered_facet(
            id, filter_field="object", facet_field="subject_category"
        )
        categories = collections.Counter(object_categories) + collections.Counter(
            subject_categories
        )
        return categories



    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: AssociationInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# def get_node_hierarchy(entity_id):
#     superClasses = f""
#
#     # query_params = {
#     #     q: str = "*:*",
#     #     offset: int = 0,
#     #     limit: int = 20,
#     #     category: str = None,
#     #     predicate: str = None,
#     #     subject: str = None,
#     #     object: str = None,
#     #     entity: str = None, # return nodes where entity is subject or object
#     #     between: str = None
#     # }
#
#     query = build_association_query(
#         {
#             #'q':'*:*',
#             "entity": f'"{entity_id}"',
#             "predicate": "biolink:same_as",
#         }
#     )
#     equivalentClasses = requests.get(f"{solr_url}/association/select{query}").json()
#
#     subClasses = ""
#     return {
#         "superClasses": superClasses,
#         "equivalentClasses": equivalentClasses,
#         "subClasses": subClasses,
#     }
