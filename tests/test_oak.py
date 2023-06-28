import pytest

from monarch_py.implementations.oak.oak_implementation import OakImplementation
from profiler import profile

@profile()
@pytest.mark.skip(reason="This is a long running test")
def test_oak():

    subject_ids = ["MP:0010771", "MP:0002169", "MP:0005391", "MP:0005389", "MP:0005367"]
    object_ids = ["HP:0004325", "HP:0000093", "MP:0006144"]

    oi = OakImplementation()
    tsps = oi.termset_pairwise_similarity(subject_ids, object_ids)


    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(tsps)
    for k in tsps:
        print(f"{k}: {type(tsps[k])}")
        if isinstance(tsps[k], dict):
            for k2 in tsps[k]:
                print(f"\t{k2}: {type(tsps[k][k2])}")

if __name__ == "__main__":
    test_oak()
