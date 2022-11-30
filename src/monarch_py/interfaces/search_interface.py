from abc import ABC, abstractmethod


class SearchInterface(ABC):
    """Abstract interface for querying the Monarch KG"""

    @abstractmethod
    def search(self, q: str, category: str, taxon: str):
        """

        Args:
            q (str): Query string to match against
            category (str): Limit results to only this category
            taxon (str): Limit results to only this taxon

        Raises:
            NotImplementedError: Use a specific implementation (see the documentation for a list of implementations)

        Returns:
            SearchResults: Dataclass representing results of a generic search.
        """
        raise NotImplementedError
