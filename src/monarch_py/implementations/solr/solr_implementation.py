import logging
from dataclasses import dataclass

from pydantic import ValidationError

from monarch_py.datamodels.model import Association, AssociationResults, Entity, EntityResults
from monarch_py.datamodels.solr import SolrQuery, core
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.service.solr_service import SolrService
from monarch_py.datamodels.solr import SolrQuery, core

from monarch_py.utilities.utils import escape

logger = logging.getLogger(__name__)


@dataclass
class SolrImplementation(
    EntityInterface, AssociationInterface, SearchInterface
):
    """Implementation of Monarch Interfaces for Solr endpoint"""

    base_url: str = "http://localhost:8983/solr"

    ###############################
    # Implements: EntityInterface #
    ###############################

    def get_entity(self, id: str) -> Entity:
        """Retrieve a specific entity by exact ID match, with optional extras

        Args:
            id (str): id of the entity to search for.
            get_association_counts (bool, optional): Whether to get association counts. Defaults to False.
            get_hierarchy (bool, optional): Whether to get the entity hierarchy. Defaults to False.

        Returns:
            Entity: Dataclass representing results of an entity search.
        """

        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        solr_document = solr.get(id)
        entity = Entity(**solr_document)
        
        # todo: make an endpoint for getting facet counts?
        # if get_association_counts:
        #    entity["association_counts"] = self.get_entity_association_counts(id)

        #        if get_hierarchy:
        #            entity["node_hierarchy"] = self.get_node_hierarchy(id)

        return entity


    ####################################
    # Implements: AssociationInterface #
    ####################################

    def get_associations(
        self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        object: str = None,
        entity: str = None,
        between: str = None,
        offset: int = 0,
        limit: int = 20,
    ) -> AssociationResults:
        """Retrieve paginated association records, with filter options

        Args:
            category (str, optional): Filter to only associations matching the specified category. Defaults to None.
            predicate (str, optional): Filter to only associations matching the specified predicate. Defaults to None.
            subject (str, optional): Filter to only associations matching the specified subject. Defaults to None.
            object (str, optional): Filter to only associations matching the specified object. Defaults to None.
            entity (str, optional): Filter to only associations where the specified entity is the subject or the object. Defaults to None.
            between (Tuple[str, str], optional): Filter to bi-directional associations between two entities.
            offset (int, optional): Result offset, for pagination. Defaults to 0.
            limit (int, optional): Limit results to specified number. Defaults to 20.

        Returns:
            AssociationResults: Dataclass representing results of an association search.
        """

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

        results = AssociationResults(associations=associations, limit=limit, offset=offset, total=total)

        return results

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def search(
            self,
            q: str = "*:*",
            category: str = None,
            taxon: str = None,
            offset: int = 0,
            limit: int = 20
    ) -> EntityResults:
        """Search for entities by label, with optional filters """

        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        query = SolrQuery(start=offset, rows=limit)

        query.q = q

        query.query_fields = "id^100 name^10 synonym"
        query.def_type = "edismax"

        if category:
            query.add_field_filter_query("category", category)
        if taxon:
            query.add_field_filter_query("in_taxon", taxon)

        query_result = solr.query(query)
        total = query_result.response.num_found

        entities = []
        for doc in query_result.response.docs:
            try:
                entity = Entity(**doc)
                entities.append(entity)
            except ValidationError:
                logger.error(f"Validation error for {doc}")
                raise

        results = EntityResults(
            limit=limit, offset=offset, total=total, entities=entities
        )

        return results

