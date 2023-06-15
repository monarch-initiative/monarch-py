import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

from loguru import logger
from pydantic import ValidationError

from monarch_py.datamodels.model import (
    Association,
    AssociationCount,
    AssociationDirectionEnum,
    AssociationResults,
    AssociationTableResults,
    DirectionalAssociation,
    Entity,
    FacetField,
    FacetValue,
    HistoBin,
    HistoPheno,
    SearchResult,
    SearchResults,
)
from monarch_py.datamodels.solr import HistoPhenoKeys, SolrQuery, core
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.service.solr_service import SolrService
from monarch_py.utils.association_type_utils import (
    AssociationTypeMappings,
    get_association_type_mapping_by_query_string,
    get_solr_query_fragment,
)
from monarch_py.utils.utils import escape


@dataclass
class SolrImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """Implementation of Monarch Interfaces for Solr endpoint"""

    base_url: str = os.getenv("MONARCH_SOLR_URL", "http://localhost:8983/solr")

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

        return entity

    ####################################
    # Implements: AssociationInterface #
    ####################################

    def get_associations(
        self,
        category: List[str] = None,
        subject: List[str] = None,
        predicate: List[str] = None,
        object: List[str] = None,
        subject_closure: str = None,
        object_closure: str = None,
        entity: List[str] = None,
        between: str = None,
        direct: bool = None,
        offset: int = 0,
        limit: int = 20,
    ) -> AssociationResults:
        """Retrieve paginated association records, with filter options

        Args:
            category: Filter to only associations matching the specified categories. Defaults to None.
            predicate: Filter to only associations matching the specified predicates. Defaults to None.
            subject: Filter to only associations matching the specified subjects. Defaults to None.
            object: Filter to only associations matching the specified objects. Defaults to None.
            subject_closure: Filter to only associations with the specified term ID as an ancestor of the subject. Defaults to None
            object_closure: Filter to only associations with the specified term ID as an ancestor of the object. Defaults to None
            entity: Filter to only associations where the specified entities are the subject or the object. Defaults to None.
            between: Filter to bi-directional associations between two entities.
            offset: Result offset, for pagination. Defaults to 0.
            limit: Limit results to specified number. Defaults to 20.

        Returns:
            AssociationResults: Dataclass representing results of an association search.
        """

        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)

        query = self._populate_association_query(
            category=category,
            predicate=predicate,
            subject=subject,
            object=object,
            subject_closure=subject_closure,
            object_closure=object_closure,
            entity=entity,
            between=between,
            direct=direct,
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
        category: List[str] = None,
        predicate: List[str] = None,
        subject: List[str] = None,
        object: List[str] = None,
        subject_closure: str = None,
        object_closure: str = None,
        entity: List[str] = None,
        between: str = None,
        direct: bool = None,
        q: str = None,
        offset: int = 0,
        limit: int = 20,
    ) -> SolrQuery:
        """Populate a SolrQuery object with association filters"""

        query = SolrQuery(start=offset, rows=limit)

        if category:
            query.add_field_filter_query("category", " OR ".join(category))
        if predicate:
            query.add_field_filter_query("predicate", " OR ".join(predicate))
        if subject:
            if direct:
                query.add_field_filter_query("subject", " OR ".join(subject))
            else:
                query.add_filter_query(
                    " OR ".join([
                        f'subject:"{s}" OR subject_closure:"{s}"'
                        for s in subject
                    ])
                )
        if subject_closure:
            query.add_field_filter_query("subject_closure", subject_closure)
        if object:
            if direct:
                query.add_field_filter_query("object", " OR ".join(object))
            else:
                query.add_filter_query(
                    " OR ".join([
                        f'object:"{o}" OR object_closure:"{o}"'
                        for o in object
                    ])
                )
        if object_closure:
            query.add_field_filter_query("object_closure", object_closure)
        if between:
            # todo: handle error reporting / parsing, think about another way to pass this?
            b = between.split(",")
            e1 = escape(b[0])
            e2 = escape(b[1])
            if direct:
                query.add_filter_query(
                    f'(subject:"{e1}" AND object:"{e2}") OR (subject:"{e2}" AND object:"{e1}")'
                )
            else:
                query.add_filter_query(
                    f'((subject:"{e1}" OR subject_closure:"{e1}") AND (object:"{e2}" OR object_closure:"{e2}")) OR ((subject:"{e2}" OR subject_closure:"{e2}") AND (object:"{e1}" OR object_closure:"{e1}"))'
                )
        if entity:
            if direct:
                query.add_filter_query(
                    " OR ".join([
                        f'subject:"{escape(entity)}" OR object:"{escape(entity)}"'
                        for e in entity
                    ])
                )
            else:
                query.add_filter_query(
                    " OR ".join([
                        f'subject:"{escape(e)}" OR subject_closure:"{escape(e)}" OR object:"{escape(e)}" OR object_closure:"{escape(e)}"'
                        for e in entity
                    ])
                )
        if q:
            # We don't yet have tokenization strategies for the association index, initially we'll limit searching to
            # the visible fields in an association table plus their ID equivalents and use a wildcard query for substring matching
            query.q = f"*{q}*"
            query.query_fields = "subject subject_label predicate object object_label"

        return query

    ###############################
    # Implements: SearchInterface #
    ###############################

    def search(
        self,
        q: str = "*:*",
        offset: int = 0,
        limit: int = 20,
        category: List[str] = None,
        in_taxon: List[str] = None,
        facet_fields: List[str] = None,
        facet_queries: List[str] = None,
        filter_queries: List[str] = None,
        sort: str = None,
    ) -> SearchResults:
        """Search for entities by label, with optional filters"""

        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        query = SolrQuery(start=offset, rows=limit, sort=sort)

        query.q = q

        query.def_type = "edismax"
        query.query_fields = self._entity_query_fields()
        query.boost = self._entity_boost()

        if category:
            query.add_filter_query(" OR ".join(f'category:"{cat}"' for cat in category))
        if in_taxon:
            query.add_filter_query(" OR ".join([f'in_taxon:"{t}"' for t in in_taxon]))
        if facet_fields:
            query.facet_fields = facet_fields
        if facet_queries:
            query.facet_queries = facet_queries
        if filter_queries:
            query.filter_queries.extend(filter_queries)

        # Search can't deal with entities that don't have names because we've made it a required field,
        # we may or may not want them in the graph and in Solr, but we can safely leave them out of
        # search
        query.add_filter_query("name:*")

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
            facet_fields=self._convert_facet_fields(
                query_result.facet_counts.facet_fields
            ),
            facet_queries=self._convert_facet_queries(
                query_result.facet_counts.facet_queries
            ),
        )

        return results

    def autocomplete(self, q: str) -> SearchResults:
        solr = SolrService(base_url=self.base_url, core=core.ENTITY)
        limit = 10
        offset = 0
        query = SolrQuery(q=q, limit=limit, offset=offset)

        query.q = q

        # match the query fields to start with
        query.query_fields = self._entity_query_fields()
        query.def_type = "edismax"

        query.boost = self._entity_boost()

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

        results = SearchResults(limit=limit, offset=offset, total=total, items=items)

        return results

    def _entity_query_fields(self):
        """
        Shared query field list between search and autocomplete, since the field list and boosts are currently the same
        """
        return "id^100 name^10 name_t^5 name_ac symbol^10 symbol_t^5 symbol_ac synonym synonym_t synonym_ac"

    def _entity_boost(self):
        """
        Shared boost function between search and autocomplete
        """
        disease_boost = 'if(termfreq(category,"biolink:Disease"),10.0,1)'
        human_gene_boost = 'if(and(termfreq(in_taxon,"NCBITaxon:9606"),termfreq(category,"biolink:Gene")),5.0,1)'

        return f"product({disease_boost},{human_gene_boost})"

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
            facet_fields=self._convert_facet_fields(
                query_result.facet_counts.facet_fields
            ),
            facet_queries=self._convert_facet_queries(
                query_result.facet_counts.facet_queries
            ),
        )

        return results

    def get_histopheno(self, subject_closure: str = None) -> HistoPheno:

        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)
        limit = 0
        offset = 0

        query = self._populate_association_query(
            subject_closure=subject_closure,
            offset=limit,
            limit=offset,
        )

        hpkeys = [i.value for i in HistoPhenoKeys]

        query.facet_queries = [f'object_closure:"{i}"' for i in hpkeys]
        query_result = solr.query(query)

        bins = []
        for k, v in query_result.facet_counts.facet_queries.items():
            id = f"{k.split(':')[1]}:{k.split(':')[2]}".replace('"', "")
            label = HistoPhenoKeys(id).name
            bins.append(HistoBin(id=id, label=label, count=v))
        bins = sorted(bins, key=lambda x: x.count, reverse=True)

        return HistoPheno(id=subject_closure, items=bins)

    def get_association_counts(self, entity: str) -> List[AssociationCount]:
        """
        Get association counts for a given entity

        This method uses chunks of solr query syntax mapped to the association type
        Args:
            entity:

        Returns:

        """
        query = self._populate_association_query(entity=entity)
        facet_queries = []
        subject_query = f'AND (subject:"{entity}" OR subject_closure:"{entity}")'
        object_query = f'AND (object:"{entity}" OR object_closure:"{entity}")'
        # Run the same facet_queries constrained to matches against either the subject or object
        # to know which kind of label will be needed in the UI to refer to the opposite side of the association
        for field_query in [subject_query, object_query]:
            for agm in AssociationTypeMappings.get_mappings():
                association_type_query = get_solr_query_fragment(agm)
                facet_queries.append(f"({association_type_query}) {field_query}")
        query.facet_queries = facet_queries
        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)
        query_result = solr.query(query)
        association_count_dict: Dict[str, AssociationCount] = {}

        for k, v in query_result.facet_counts.facet_queries.items():
            if v > 0:
                if k.endswith(subject_query):
                    original_query = (
                        k.replace(f" {subject_query}", "").lstrip("(").rstrip(")")
                    )
                    agm = get_association_type_mapping_by_query_string(original_query)
                    label = agm.object_label
                elif k.endswith(object_query):
                    original_query = (
                        k.replace(f" {object_query}", "").lstrip("(").rstrip(")")
                    )
                    agm = get_association_type_mapping_by_query_string(original_query)
                    label = agm.subject_label
                    # always use forward for symmetric association types
                else:
                    raise ValueError(
                        f"Unexpected facet query when building association counts: {k}"
                    )
                # Symmetric associations need to be summed together, since both directions will be returned
                # when searching for associations by type
                if label in association_count_dict and agm.symmetric:
                    association_count_dict[label].count += v
                else:
                    association_count_dict[label] = AssociationCount(
                        label=label,
                        count=v,
                        category=agm.category,
                    )

        association_counts: List[AssociationCount] = list(
            association_count_dict.values()
        )
        return association_counts

    def get_association_table(
        self,
        entity: str,
        category: str,
        q=None,
        sort=None,
        offset=0,
        limit=5,
    ) -> AssociationTableResults:
        if sort:
            raise NotImplementedError("Sorting is not yet implemented")

        query = self._populate_association_query(
            entity=entity,
            category=category,
            q=q,
            offset=offset,
            limit=limit,
        )
        solr = SolrService(base_url=self.base_url, core=core.ASSOCIATION)
        query_result = solr.query(query)
        total = query_result.response.num_found
        associations: List[DirectionalAssociation] = []
        for doc in query_result.response.docs:
            try:
                direction = self._get_association_direction(entity, doc)
                association = DirectionalAssociation(**doc, direction=direction)
                associations.append(association)
            except ValidationError:
                logger.error(f"Validation error for {doc}")
                raise

        results = AssociationResults(
            items=associations, limit=limit, offset=offset, total=total
        )

        return results

    def _get_association_direction(
        self, entity: str, document: Dict
    ) -> AssociationDirectionEnum:
        if document.get("subject") == entity or (
            document.get("subject_closure")
            and entity in document.get("subject_closure")
        ):
            direction = AssociationDirectionEnum.outgoing
        elif document.get("object") == entity or (
            document.get("object_closure") and entity in document.get("object_closure")
        ):
            direction = AssociationDirectionEnum.incoming
        else:
            raise ValueError(f"Entity {entity} not found in association {document}")
        return direction

    def _convert_facet_fields(self, solr_facet_fields: Dict) -> List[FacetField]:
        """
        Converts a list of raw solr facet fields from the solr response to a list of
        FacetField instances

        Args:
            facet_fields (Dict): A list of facet fields from the solr response

        Returns:
            List[FacetField]: A list of FacetField instances, with FacetValues populated within
        """

        facet_fields: List[FacetField] = []
        for field in solr_facet_fields:
            ff = FacetField(label=field)
            facet_list = solr_facet_fields[field]
            facet_dict = dict(zip(facet_list[::2], facet_list[1::2]))
            ff.facet_values = [
                FacetValue(label=k, count=v) for k, v in facet_dict.items()
            ]
            facet_fields.append(ff)

        return facet_fields

    def _convert_facet_queries(
        self, solr_facet_queries: Dict[str, int]
    ) -> List[FacetValue]:
        """
        Converts a list of raw solr facet queries from the solr response to a list of
        FacetValue instances

        Args:
            facet_queries (Dict): A dictionary of facet queries from the solr response

        Returns:
            List[FacetValue]: A list of FacetValue instances
        """

        facet_values = [
            FacetValue(label=k, count=v) for k, v in solr_facet_queries.items()
        ]
        return facet_values

    def solr_is_available(self):
        import requests

        try:
            response = requests.get(self.base_url)
            return response.status_code == 200
        except Exception:
            return False
