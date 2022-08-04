import requests, collections
from monarch_py.query import *

solr_url = "http://localhost:8983/solr"
association_url = "http://localhost:8983/solr/association"
entity_url = "http://localhost:8983/solr/entity"

def strip_json(doc: dict, *fields_to_remove: str):
    for field in fields_to_remove:
        try:
            del doc[field]
        except:
            pass
    return doc


def get_filtered_facet(entity_id, filter_field, facet_field):
    response = requests.get(f"{association_url}/select?q=*:*&limit=0&facet=true&facet.field={facet_field}&fq={filter_field}:\"{entity_id}\"")
    facet_fields = response.json()["facet_counts"]["facet_fields"][facet_field]
    
    return dict(zip(facet_fields[::2], facet_fields[1::2]))


def get_entity_association_counts(entity_id):
    object_categories = get_filtered_facet(entity_id, filter_field="subject", facet_field="object_category")
    subject_categories = get_filtered_facet(entity_id, filter_field="object", facet_field="subject_category")
    categories = collections.Counter(object_categories) + collections.Counter(subject_categories)
    return categories

def get_node_hierarchy(entity_id):
    superClasses = f''
    
    # query_params = {
    #     q: str = "*:*",
    #     offset: int = 0,
    #     limit: int = 20,
    #     category: str = None,
    #     predicate: str = None,
    #     subject: str = None,
    #     object: str = None,
    #     entity: str = None, # return nodes where entity is subject or object
    #     between: str = None
    # }

    query = build_association_query(
        {
            #'q':'*:*',
            'entity':f'"{entity_id}"',
            'predicate':'biolink:same_as'
        }
    )
    equivalentClasses = requests.get(f'{solr_url}/association/select{query}').json()

    subClasses = ''
    return {'superClasses': superClasses, 'equivalentClasses': equivalentClasses, 'subClasses':subClasses}