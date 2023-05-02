from abc import ABC, abstractmethod
from typing import List, Tuple

from monarch_py.datamodels.model import AssociationTypeEnum, FacetValue, SearchResults


class SearchInterface(ABC):
    """Abstract interface for searching the Monarch KG in a Lucene way"""

    @abstractmethod
    def search(
        self,
        q: str,
        category: str,
        taxon: str,
        offset: int = 0,
        limit: int = 20,
        facet_fields: List[str] = None,
        filter_queries: List[str] = None,
        facet_queries: List[str] = None,
    ) -> SearchResults:
        """

        Args:
            q (str): Query string to match against
            category (str): Limit results to only this category
            taxon (str): Limit results to only this taxon
            offset (int): Offset of the first result to return, defaults to 0
            limit (int): Limit the number of results to return, defaults to 20

        Raises:
            NotImplementedError: Use a specific implementation (see the documentation for a list of implementations)

        Returns:
            EntityResults: Dataclass representing results of a generic entity search.
        """
        raise NotImplementedError

    def autocomplete(self, q: str) -> SearchResults:
        """

        Args:
            q (str): Query string to match against

        Raises:
            NotImplementedError: Use a specific implementation (see the documentation for a list of implementations)

        Returns:
            SearchResults: Dataclass representing results of a generic entity search.
        """
        raise NotImplementedError

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
        association_type: AssociationTypeEnum = None,
    ) -> SearchResults:
        """
        Get facet counts and facet query counts for associations
        Args:
            facet_fields (List[str]): Facet fields to return counts for
            facet_queries (List[str]): Facet queries to return counts for
            category (str): Filter to only associations matching the specified category
            predicate (str): Filter to only associations matching the specified predicate
            subject (str): Filter to only associations matching the specified subject
            subject_closure (str): Filter to only associations with the specified term ID as an ancestor of the subject
            object (str): Filter to only associations matching the specified object
            object_closure (str): Filter to only associations with the specified term ID as an ancestor of the object
            entity (str): Filter to only associations where the specified entity is the subject or the object
            between (Tuple[str, str]): Filter to bi-directional associations between two entities
        Returns:
            SearchResults: Dataclass representing results of a search, with zero rows returned but total count
            and faceting information populated
        """
        raise NotImplementedError

    def get_association_counts(self, entity: str) -> List[FacetValue]:
        """
        Get counts of associations for a given entity
        Args:
            entity (str): Entity to get association counts for
        Returns:
            List[FacetValue]: List of FacetValue objects representing the counts of associations for the given entity
        """
        raise NotImplementedError
