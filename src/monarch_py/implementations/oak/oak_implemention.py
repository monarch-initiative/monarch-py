from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface

@dataclass
class OakImplementation():
    """Implementation of Monarch Interfaces for OAK"""

    def __int__(self):
        # get an oi
        self.oi = somehow_get_an_oi() # SemanticSimilarityInterface
        pass

    def termset_pairwise_similarity(ts1, ts2, predicates=None, labels=False) -> float:
        sim = self.oi.termset_pairwise_similarity(ts1, ts2, predicates=predicates, labels=labels)
        return sim
