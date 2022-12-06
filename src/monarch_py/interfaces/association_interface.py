from abc import ABC, abstractmethod
from typing import Tuple

from monarch_py.datamodels.model import AssociationResults


class AssociationInterface(ABC):
    """Abstract interface for associations in the Monarch KG"""

    @abstractmethod
    def get_associations(
        self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        object: str = None,
        entity: str = None,
        between: Tuple[str, str] = None,
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

        Raises:
            NotImplementedError: Use a specific implementation (see the documentation for a list of implementations)

        Returns:
            [AssociationResults](): Dataclass representing results of an association search.
        """
        raise NotImplementedError
