from dataclasses import dataclass
# from typing import Iterable, List

from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
# from oaklib.datamodels.similarity import TermSetPairwiseSimilarity
from oaklib.selector import get_adapter


@dataclass
class OakImplementation(SemanticSimilarityInterface):
    """Implementation of Monarch Interfaces for OAK

    Notes:
        - This is an in-progress conversion to OAK
        - Biolink-API call args:
            - reference_ids -> subject_ids
            - query_ids -> object_ids
            - is_feature_set = ??
    """
    oi = get_adapter(f"sqlite:obo:phenio") 


    def termset_pairwise_similarity(self, ts1, ts2, predicates=None, labels=False) -> float:
        sim = self.oi.termset_pairwise_similarity(ts1, ts2, predicates=predicates, labels=labels)
        return sim
