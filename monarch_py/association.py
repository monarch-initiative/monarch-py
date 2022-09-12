from monarch_py.utilities.utils import *
from monarch_py.query import *


def get_associations(
    q: str = "*:*",
    offset: int = 0,
    limit: int = 20,
    category: str = None,
    predicate: str = None,
    subject: str = None,
    object: str = None,
    entity: str = None,  # return nodes where entity is subject or object
    between: str = None,  # strip by comma and check associations in both directions. example: "MONDO:000747,MONDO:000420"
):
    query = build_association_query(
        q=q,
        offset=offset,
        limit=limit,
        category=category,
        predicate=predicate,
        subject=subject,
        object=object,
        entity=entity,
        between=between,
    )
    association_url = f"{solr_url}/association/query"
    url = association_url + query
    r = requests.get(url)
    results = r.json()["response"]["docs"]
    for i in results:
        strip_json(i, "_version_")
    return results
