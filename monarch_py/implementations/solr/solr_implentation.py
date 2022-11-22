import collections
import logging
from dataclasses import dataclass

from pydantic import ValidationError

from monarch_py.datamodels.model import Association, AssociationResults, Entity
from monarch_py.datamodels.solr import SolrQuery, core
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.service.solr_service import SolrService
from monarch_py.utilities.utils import escape

logger = logging.getLogger(__name__)


@dataclass
class SolrImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """
    Wraps the Monarch Solr endpoint
    """

    base_url: str = "http://localhost:8983/solr"

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: EntityInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_entity(
        self, id: str, get_association_counts: bool = False, get_hierarchy: bool = False
    ) -> Entity:

        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        solr_document = solr.get(id)
        entity = Entity(**solr_document)

        # todo: make an endpoint for getting facet counts?
        # if get_association_counts:
        #    entity["association_counts"] = self.get_entity_association_counts(id)

        #        if get_hierarchy:
        #            entity["node_hierarchy"] = self.get_node_hierarchy(id)

        return entity

    def get_entity_association_counts(self, id: str):

        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)

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

    def get_associations(
        self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        object: str = None,
        entity: str = None,  # return nodes where entity is subject or object
        between: str = None,
        offset: int = 1,
        limit: int = 20,
    ) -> AssociationResults:
        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)
        query = SolrQuery(start=offset, rows=limit)

        if category:
            query.add_field_filter_query("category", category)
        if predicate:
            query.add_field_filter_query("predicate", predicate)
        if subject:
            query.add_field_filter_query("subject", subject)
        if object:
            query.add_field_filter_query("object", object)
        if between:
            # todo: handle error reporting / parsing, think about another way to pass this?
            b = between.split(",")
            e1 = escape(b[0])
            e2 = escape(b[1])
            query.add_filter_query(
                f'(subject:"{e1}" AND object:"{e2}") OR (subject:"{e2}" AND object:"{e1}")'
            )
        if entity:
            query.add_filter_query(
                f'subject:"{escape(entity)}" OR object:"{escape(entity)}"'
            )

        query_result = solr.query(query)
        total = query_result.response.num_found

        associations = []
        for doc in query_result.response.docs:
            try:
                association = Association(**doc)
                associations.append(association)
            except ValidationError:
                logger.error(f"Validation error for {doc}")
                raise

        results = AssociationResults(
            limit=limit, offset=offset, total=total, associations=associations
        )

        return results

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
