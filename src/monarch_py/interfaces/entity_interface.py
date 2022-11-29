from abc import ABC

from monarch_py.datamodels.model import Entity


class EntityInterface(ABC):
    def get_entity(
        self, id: str, get_association_counts: bool = False, get_hierarchy: bool = False
    ) -> Entity:
        """
        Retrieve a specific entity by exact ID match, with optional extras

        :param id:
        :param get_association_counts:
        :param get_hierarchy:
        :return:
        """
        raise NotImplementedError
