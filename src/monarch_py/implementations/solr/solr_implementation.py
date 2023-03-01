import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

from pydantic import ValidationError

from monarch_py.datamodels.model import (
    Association,
    AssociationResults,
    Entity,
    FacetField,
    FacetValue,
    SearchResult,
    SearchResults,
)
from monarch_py.datamodels.solr import SolrQuery, core
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.service.solr_service import SolrService
from monarch_py.utilities.utils import escape

logger = logging.getLogger(__name__)


@dataclass
class SolrImplementation(EntityInterface, AssociationInterface, SearchInterface):
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
        subject_closure: str = None,
        object: str = None,
        object_closure: str = None,
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
            subject_closure (str, optional): Filter to only associations with the specified term ID as an ancestor of the subject. Defaults to None
            object (str, optional): Filter to only associations matching the specified object. Defaults to None.
            object_closure (str, optional): Filter to only associations with the specified term ID as an ancestor of the object. Defaults to None
            entity (str, optional): Filter to only associations where the specified entity is the subject or the object. Defaults to None.
            between (Tuple[str, str], optional): Filter to bi-directional associations between two entities.
            offset (int, optional): Result offset, for pagination. Defaults to 0.
            limit (int, optional): Limit results to specified number. Defaults to 20.

        Returns:
            AssociationResults: Dataclass representing results of an association search.
        """

        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)

        query = self._populate_association_query(
            category=category,
            predicate=predicate,
            subject=subject,
            subject_closure=subject_closure,
            object=object,
            object_closure=object_closure,
            entity=entity,
            between=between,
            offset=offset,
            limit=limit,
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
            items=associations, limit=limit, offset=offset, total=total
        )

        return results

    def _populate_association_query(
        self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        subject_closure: str = None,
        object: str = None,
        object_closure: str = None,
        entity: str = None,
        between: str = None,
        offset: int = 0,
        limit: int = 20,
    ) -> SolrQuery:
        """
        Populate a SolrQuery object with association filters
        Args:
            category (str, optional): Filter to only associations matching the specified category. Defaults to None.
            predicate (str, optional): Filter to only associations matching the specified predicate. Defaults to None.
            subject (str, optional): Filter to only associations matching the specified subject. Defaults to None.
            subject_closure (str, optional): Filter to only associations with the specified term ID as an ancestor of the subject. Defaults to None
            object (str, optional): Filter to only associations matching the specified object. Defaults to None.
            object_closure (str, optional): Filter to only associations with the specified term ID as an ancestor of the object. Defaults to None
            entity (str, optional): Filter to only associations where the specified entity is the subject or the object. Defaults to None.
            between (Tuple[str, str], optional): Filter to bi-directional associations between two entities.
            offset (int, optional): Result offset, for pagination. Defaults to 0.
            limit (int, optional): Limit results to specified number. Defaults to 20.

        Returns:
            SolrQuery: A populated SolrQuery object
        """
        query = SolrQuery(start=offset, rows=limit)

        if category:
            query.add_field_filter_query("category", category)
        if predicate:
            query.add_field_filter_query("predicate", predicate)
        if subject:
            query.add_field_filter_query("subject", subject)
        if subject_closure:
            query.add_field_filter_query("subject_closure", subject_closure)
        if object:
            query.add_field_filter_query("object", object)
        if object_closure:
            query.add_field_filter_query("object_closure", object_closure)
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

        return query

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def search(
        self,
        q: str = "*:*",
        category: str = None,
        taxon: str = None,
        offset: int = 0,
        limit: int = 20,
        # add a facet_fields params defaulting to an empty list
        facet_fields: List[str] = None,
        filter_queries: List[str] = None,
        facet_queries: List[str] = None,
    ) -> SearchResults:
        """Search for entities by label, with optional filters"""

        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        query = SolrQuery(start=offset, rows=limit)

        query.q = q

        query.query_fields = "id^100 name^10 name_t^5 name_ac symbol^10 symbol_t^5 synonym synonym_t synonym_ac"
        query.def_type = "edismax"

        if facet_fields:
            query.facet_fields = facet_fields
        if facet_queries:
            query.facet_queries = facet_queries

        if category:
            query.add_field_filter_query("category", category)
        if taxon:
            query.add_field_filter_query("in_taxon", taxon)
        if filter_queries:
            query.filter_queries.extend(filter_queries)

        query_result = solr.query(query)
        total = query_result.response.num_found

        items = []
        for doc in query_result.response.docs:
            try:
                result = SearchResult(**doc)
                items.append(result)
            except ValidationError:
                logger.error(f"Validation error for {doc}")
                raise

        results = SearchResults(
            limit=limit,
            offset=offset,
            total=total,
            items=items,
            facet_fields=query_result.facet_counts.facet_fields,
            facet_queries=query_result.facet_counts.facet_queries,
        )

        return results

    def get_association_facets(
        self,
        facet_fields: List[str] = None,
        facet_queries: List[str] = None,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        subject_closure: str = None,
        object: str = None,
        object_closure: str = None,
        entity: str = None,
        between: Tuple[str, str] = None,
    ) -> SearchResults:

        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)
        limit = 0
        offset = 0
        query = self._populate_association_query(
            category=category,
            predicate=predicate,
            subject=subject,
            subject_closure=subject_closure,
            object=object,
            object_closure=object_closure,
            entity=entity,
            between=between,
            offset=limit,
            limit=offset,
        )

        query.facet_fields = facet_fields
        query.facet_queries = facet_queries

        query_result = solr.query(query)
        total = query_result.response.num_found

        results = SearchResults(
            limit=limit,
            offset=offset,
            total=total,
            items=[],
            facet_fields=self.convert_facet_fields(
                query_result.facet_counts.facet_fields
            ),
            facet_queries=self.convert_facet_queries(
                query_result.facet_counts.facet_queries
            ),
        )

        return results

    def convert_facet_fields(self, solr_facet_fields: Dict) -> Dict[str, FacetField]:
        """
        Converts a list of raw solr facet fields from the solr response to a list of
        FacetField instances

        Args:
            facet_fields (Dict): A list of facet fields from the solr response

        Returns:
            List[FacetField]: A list of FacetField instances, with FacetValues populated within
        """

        facet_fields: Dict[str, FacetField] = {}
        for field in solr_facet_fields:
            ff = FacetField(label=field)
            facet_list = solr_facet_fields[field]
            facet_dict = dict(zip(facet_list[::2], facet_list[1::2]))
            ff.facet_values = {
                k: FacetValue(label=k, count=v) for k, v in facet_dict.items()
            }
            facet_fields[field] = ff

        return facet_fields

    def convert_facet_queries(
        self, solr_facet_queries: Dict[str, int]
    ) -> Dict[str, FacetValue]:
        """
        Converts a list of raw solr facet queries from the solr response to a list of
        FacetValue instances

        Args:
            facet_queries (Dict): A dictionary of facet queries from the solr response

        Returns:
            List[FacetValue]: A list of FacetValue instances
        """

        facet_values = {
            k: FacetValue(label=k, count=v) for k, v in solr_facet_queries.items()
        }
        return facet_values
