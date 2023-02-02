from dataclasses import dataclass
import logging

from pydantic import ValidationError
import pystow

from monarch_py.datamodels.model import Association, AssociationResults, Entity
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.utilities.utils import dict_factory, escape, SQL_DATA_URL

logger = logging.getLogger(__name__)

monarchstow = pystow.module("monarch")


@dataclass
class SQLImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """Implementation of Monarch Interfaces for SQL endpoint"""

    ###############################
    # Implements: EntityInterface #
    ###############################

    def get_entity(self, id: str, update: bool = False) -> Entity:
        """Retrieve a specific entity by exact ID match, writh optional extras

        Args:
            id (str): id of the entity to search for.
            get_association_counts (bool, optional): Whether to get association counts. Defaults to False.
            get_hierarchy (bool, optional): Whether to get the entity hierarchy. Defaults to False.

        Returns:
            Entity: Dataclass representing results of an entity search.
        """
        # TODO: Implement association counts and heirarchy

        with monarchstow.ensure_open_sqlite_gz("sql", url=SQL_DATA_URL, force=update) as db:
            db.row_factory = dict_factory      
            cur = db.cursor()
            result = cur.execute(f"SELECT * FROM nodes WHERE id = '{id}'").fetchone()

        if not result:
            return None
        params = {
                'id': result['id'],
                'category': result['category'].split("|"),
                'name': result['name'],
                'description': result['description'],
                'xref': result['xref'].split("|"),
                'provided_by': result['provided_by'],
                'in_taxon': result['in_taxon'],
                'symbol': result['symbol'],
                'type': result['type'],
                'synonym': result['synonym'].split("|")
            }
        try:
            params['source'] = result['source']
        except KeyError:
            pass
        # Convert empty strings to null value
        for p in params:
            params[p] = None if not params[p] else params[p]

        try:
            entity = Entity(**params)     
        except ValidationError:
            logger.error(f"Validation error for {result}")
            raise
        return entity
    
    ####################################
    # Implements: AssociationInterface #
    ####################################

    def get_associations(self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        object: str = None,
        entity: str = None,
        between: str = None,
        offset: int = 0,
        limit: int = 20,
        update: bool = False,
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
                
        clauses = []
        if category:
            clauses.append(f"category = '{category}'")
        if predicate:
            clauses.append(f"predicate = '{predicate}'")
        if subject:
            clauses.append(f"subject = '{subject}'")
        if object:
            clauses.append(f"object = '{object}'")
        if entity:
            clauses.append(f"subject = '{entity}' OR object = '{entity}'")
        if between:
            # todo: handle error reporting / parsing, think about another way to pass this?
            b = between.split(",")
            e1 = b[0]
            e2 = b[1]
            clauses.append(f"subject = '{e1}' AND object = '{e2}' OR subject = '{e2}' AND object = '{e1}'")

        query = f"SELECT * FROM edges "
        if clauses:
            query += "WHERE " + " AND ".join(clauses)
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        count_query = f"SELECT COUNT(*) FROM edges "
        if clauses:
            count_query += "WHERE " + " AND ".join(clauses)
        
        with monarchstow.ensure_open_sqlite_gz("sql", url=SQL_DATA_URL, force=update) as db:
            db.row_factory = dict_factory      
            cur = db.cursor()
            results = cur.execute(query).fetchall()
            count = cur.execute(count_query).fetchone()
            total = count[f"COUNT(*)"]
        
        associations = []
        for row in results:
            params = {
                'id': row['id'],
                'original_subject': row['original_subject'],
                'predicate': row['predicate'],
                'original_object': row['original_object'],
                'category': row['category'].split("|"),
                'aggregator_knowledge_source': row['aggregator_knowledge_source'].split("|"),
                'primary_knowledge_source': row['primary_knowledge_source'].split("|"),
                'publications': row['publications'].split("|"),
                'qualifiers': row['qualifiers'].split("|"),
                'provided_by': row['provided_by'],
                'has_evidence': row['has_evidence'],
                'stage_qualifier': row['stage_qualifier'],
                'relation': row['relation'],
                'knowledge_source': row['knowledge_source'].split("|"),
                'negated': False if not row['negated'] else True,
                'frequency_qualifier': row['frequency_qualifier'],
                'onset_qualifier': row['onset_qualifier'],
                'sex_qualifier': row['sex_qualifier'],
                'subject': row['subject'],
                'object': row['object']
            }
            # Convert empty strings to null value
            for p in params:
                params[p] = None if not params[p] else params[p]
            try:
                associations.append(Association(**params))
            except ValidationError:
                logger.error(f"Validation error for {row}")
                raise

        results = AssociationResults(associations=associations, limit=limit, offset=offset, total=total)
        return results

    def search(self):
        """Not Implemented"""
        ...