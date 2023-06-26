# from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
# from oaklib.selector import get_adapter

# oi = get_adapter(f"sqlite:obo:phenio")

# subject_ids = ["MP:0010771", "MP:0002169", "MP:0005391", "MP:0005389", "MP:0005367"]
# object_ids = ["HP:0004325", "HP:0000093", "MP:0006144"]

# tsps = oi.termset_pairwise_similarity(subject_ids, object_ids)
# print(tsps)

from monarch_py.implementations.oak.oak_implementation import OakImplementation

oi = OakImplementation()

subject_ids = ["MP:0010771", "MP:0002169", "MP:0005391", "MP:0005389", "MP:0005367"]
object_ids = ["HP:0004325", "HP:0000093", "MP:0006144"]

tsps = oi.termset_pairwise_similarity(subject_ids, object_ids)
print(tsps)