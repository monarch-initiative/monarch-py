from dataclasses import dataclass
from typing import Iterable, List

from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.datamodels.similarity import TermSetPairwiseSimilarity
from oaklib.types import CURIE, PRED_CURIE


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
    semsim = SemanticSimilarityInterface()


    def common_ancestors(self, subject: CURIE, object: CURIE, predicates: List[PRED_CURIE] = None, subject_ancestors: List[CURIE] = None, object_ancestors: List[CURIE] = None, include_owl_thing: bool = True) -> Iterable[CURIE]:
        return super().common_ancestors(subject, object, predicates, subject_ancestors, object_ancestors, include_owl_thing)


    def termset_pairwise_similarity(self, ts1, ts2, predicates=None, labels=False) -> float:
        sim = self.semsim.termset_pairwise_similarity(ts1, ts2, predicates=predicates, labels=labels)
        return sim
