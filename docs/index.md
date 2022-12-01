# monarch-py

## Introduction  

`monarch-py` is a Python API for interacting with and querying the  
Monarch knowledge graph, with implementations for Solr and Sqlite backends.  
This means the same API methods can be used regardless of the implementation.  
This library provides a collection of interfaces for graph operations such as retrieving entities and browsing associations. 

## Installation

Requires Python 3.8 or higher

This library is available through PyPi:
```python
pip install monarch-py
```

## Basic Example

```python
>>> from monarch_py.implementations.solr.solr_implentation import SolrImplementation
>>> si = SolrImplementation()
>>> entity = si.get_entity("MONDO:0007947")
>>> print(entity.name)
"Marfan syndrome"

>>> response = si.get_associations(predicate="biolink:has_phenotype")
>>> print(response.total > 600000)
True
>>> print("biolink:has_phenotype" in response.associations[0].predicate)
True
```
