from dataclasses import dataclass
import logging
from pathlib import Path
import sqlite3

from pydantic import ValidationError

from monarch_py.datamodels.model import Association, AssociationResults, Entity, EntityResults
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.interfaces.search_interface import SearchInterface
from monarch_py.utilities.utils import escape

logger = logging.getLogger(__name__)


@dataclass
class SQLImplementation(EntityInterface, AssociationInterface, SearchInterface):
    """Implementation of Monarch Interfaces for SQL endpoint"""

    db = Path(__file__).parent.parent.parent / "data" / "sql" / "monarch-kg.db"
    
    def get_cursor(self):
        con = sqlite3.connect(self.db)

        # # provides both index-based and case-insensitive name-based access to columns
        # con.row_factory = sqlite3.Row 

        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}
        
        con.row_factory = dict_factory

        return con.cursor()

    ###############################
    # Implements: EntityInterface #
    ###############################

    def get_entity(self, id: str) -> Entity:
        """Retrieve a specific entity by exact ID match, writh optional extras

        Args:
            id (str): id of the entity to search for.
            get_association_counts (bool, optional): Whether to get association counts. Defaults to False.
            get_hierarchy (bool, optional): Whether to get the entity hierarchy. Defaults to False.

        Returns:
            Entity: Dataclass representing results of an entity search.
        """
        # TODO: Implement association counts and heirarchy

        cur = self.get_cursor()
        result = cur.execute(f"SELECT * FROM nodes WHERE id = '{id}'").fetchone()
        entity = Entity(
            id = result['id'],
            category = result['category'].split("|"),
            name = result['name'],
            description = result['description'],
            xref = result['xref'].split("|"),
            provided_by = result['provided_by'],
            in_taxon = result['in_taxon'],
            source = result['source'],
            symbol = result['symbol'],
            type = result['type'],
            synonym = result['synonym'].split("|")
        )
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
        
        cur = self.get_cursor()
        
        clauses = []
        if category:
            clauses.append(f"category = '{category}'")
        if predicate:
            clauses.append(f"prediate = '{predicate}'")
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

        clauses = " AND ".join(clauses)
        query = f"SELECT * FROM edges WHERE {clauses}"
        if limit:
            query += f" LIMIT {limit}"
        results = cur.execute(query).fetchall()

        total = len(results)
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

        results = AssociationResults(limit=limit, total=total, associations=associations)
        return results

    def search(self):
        """Not Implemented"""
        ...