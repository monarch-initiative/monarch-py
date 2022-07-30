import requests, collections

solr_url = "http://localhost:8983/solr"
association_url = "http://localhost:8983/solr/association"


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
    superClasses = f''# some solr query

    # equivalentClasses = requests.get(f'{solr_url}/entity/select?q=*:*&facet.field=predicate&fq=biolink\:same_as:\"{entity_id}\"').json() # some solr query
    equivalentClasses = requests.get(f'{solr_url}/entity/get?id={entity_id}&fq=predicate:biolink\:same_as').json() # some solr query
    # equivalentClasses = get_filtered_facet(entity_id, 'predicate', 'biolink\:same_as')

    subClasses = ''# some solr query 
    return {'superClasses': superClasses, 'equivalentClasses': equivalentClasses, 'subClasses':subClasses}