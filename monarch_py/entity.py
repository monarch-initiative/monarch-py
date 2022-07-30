import requests

from monarch_py.utils import *

def get_entity(
    id, 
    get_association_counts: bool = False,
    get_hierarchy: bool = True):
    url = f"{solr_url}/entity/get?id={id}"
    r = requests.get(url)
    entity = r.json()['doc']
    strip_json(entity, "_version_")

    if get_association_counts:
        association_counts = get_entity_association_counts(id)
        entity["association_counts"] = association_counts

    if get_hierarchy:
        entity['node_hierarchy'] = get_node_hierarchy(id)

    return entity['node_hierarchy']
    return entity

