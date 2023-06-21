from dataclasses import dataclass
from typing import List

import pystow
from loguru import logger
from pydantic import ValidationError

from monarch_py.datamodels.model import Association, AssociationResults, Entity
from monarch_py.interfaces.association_interface import AssociationInterface
from monarch_py.interfaces.entity_interface import EntityInterface
from monarch_py.utils.utils import SQL_DATA_URL, dict_factory

monarchstow = pystow.module("monarch")


@dataclass
class SQLImplementation(EntityInterface, AssociationInterface):
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

        with monarchstow.ensure_open_sqlite_gz(
            "sql", url=SQL_DATA_URL, force=update
        ) as db:
            db.row_factory = dict_factory
            cur = db.cursor()
            result = cur.execute(f"SELECT * FROM nodes WHERE id = '{id}'").fetchone()

        if not result:
            return None
        params = {
            "id": result["id"],
            "category": result["category"].split("|"),
            "name": result["name"],
            "description": result["description"],
            "xref": result["xref"].split("|"),
            "provided_by": result["provided_by"],
            "in_taxon": result["in_taxon"],
            "symbol": result["symbol"],
            "type": result["type"],
            "synonym": result["synonym"].split("|"),
        }
        try:
            params["source"] = result["source"]
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

    def get_associations(
        self,
        category: List[str] = None,
        subject: List[str] = None,
        predicate: List[str] = None,
        object: List[str] = None,
        subject_closure: str = None,
        object_closure: str = None,
        entity: List[str] = None,
        direct: bool = None,
        offset: int = 0,
        limit: int = 20,
    ) -> AssociationResults:
        """Retrieve paginated association records, with filter options

        Args:
            category (str, optional): Filter to only associations matching the specified category. Defaults to None.
            predicate (str, optional): Filter to only associations matching the specified predicate. Defaults to None.
            subject (str, optional): Filter to only associations matching the specified subject. Defaults to None.
            object (str, optional): Filter to only associations matching the specified object. Defaults to None.
            subject_closure (str, optional): Filter to only associations with the specified term ID as an ancestor of the subject. Defaults to None.
            object_closure (str, optional): Filter to only associations the specified term ID as an ancestor of the object. Defaults to None.
            entity (str, optional): Filter to only associations where the specified entity is the subject or the object. Defaults to None.
            association_type (str, optional): Filter to only associations matching the specified association label. Defaults to None.
            offset (int, optional): Result offset, for pagination. Defaults to 0.
            limit (int, optional): Limit results to specified number. Defaults to 20.

        Returns:
            AssociationResults: Dataclass representing results of an association search.
        """

        clauses = []
        if category:
            clauses.append(" OR ".join([f"category = '{c}'" for c in category]))
        if subject:
            clauses.append(" OR ".join([f"subject = '{s}'" for s in subject]))
        if predicate:
            clauses.append(" OR ".join([f"predicate = '{p}'" for p in predicate]))
        if object:
            clauses.append(" OR ".join([f"object = '{o}'" for o in object]))
        if subject_closure:
            clauses.append(f"subject_closure like '%{subject_closure}%'")
        if object_closure:
            clauses.append(f"object_closure like '%{object_closure}%'")
        if entity:
            clauses.append(
                " OR ".join([f"subject = '{e}' OR object = '{e}'" for e in entity])
            )
        
        query = f"SELECT * FROM denormalized_edges "
        if clauses:
            query += "WHERE " + " AND ".join(clauses)
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        count_query = f"SELECT COUNT(*) FROM denormalized_edges "
        if clauses:
            count_query += "WHERE " + " AND ".join(clauses)

        with monarchstow.ensure_open_sqlite_gz(
            "sql", url=SQL_DATA_URL
        ) as db:
            db.row_factory = dict_factory
            cur = db.cursor()
            results = cur.execute(query).fetchall()
            count = cur.execute(count_query).fetchone()
            total = count[f"COUNT(*)"]

        associations = []
        for row in results:
            result = {
                "id": row["id"],
                "original_subject": row["original_subject"],
                "predicate": row["predicate"],
                "original_object": row["original_object"],
                "category": row["category"],
                "aggregator_knowledge_source": row["aggregator_knowledge_source"].split("|"),
                "primary_knowledge_source": row["primary_knowledge_source"].split("|"),
                "publications": row["publications"].split("|"),
                "qualifiers": row["qualifiers"].split("|"),
                "provided_by": row["provided_by"],
                "has_evidence": row["has_evidence"],
                "stage_qualifier": row["stage_qualifier"],
                "relation": row["relation"],
                "negated": False if not row["negated"] else True,
                "frequency_qualifier": row["frequency_qualifier"],
                "onset_qualifier": row["onset_qualifier"],
                "sex_qualifier": row["sex_qualifier"],
                "subject": row["subject"],
                "object": row["object"],
            }
            # Convert empty strings to null value
            for key in result:
                result[key] = None if not result[key] else result[key]
            try:
                associations.append(Association(**result))
            except ValidationError:
                logger.error(f"Validation error for {row}")
                raise

        results = AssociationResults(
            items=associations, limit=limit, offset=offset, total=total
        )
        return results
