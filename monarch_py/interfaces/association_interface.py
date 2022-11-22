from abc import ABC

from monarch_py.datamodels.model import AssociationResults


class AssociationInterface(ABC):
    def get_associations(
        self,
        category: str = None,
        predicate: str = None,
        subject: str = None,
        object: str = None,
        entity: str = None,  # return nodes where entity is subject or object
        between: str = None,
        page: int = 0,
        limit: int = 20,
    ) -> AssociationResults:
        """

        Retrieve paginated association records, with filter options

        :param category: filter to only associations matching the specified category
        :param predicate: filter to only associations matching the specified predicate
        :param subject: filter to only associations matching the specified subject
        :param object: filter to only associations matching the specified object
        :param entity: filter to only associations where the specified entity is the subject or the object
        :param between: filter to only associations between the specified entities
        :param page:
        :param limit:
        :return:
        """
        raise NotImplementedError
