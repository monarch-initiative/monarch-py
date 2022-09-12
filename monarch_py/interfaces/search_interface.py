from abc import ABC


class SearchInterface(ABC):
    def search(self, q: str, category: str, taxon: str):
        """

        :param q: Query string to match against
        :param category: Limit results to only this category
        :param taxon: Limit results to only this taxon
        :return:
        """
        raise NotImplementedError
