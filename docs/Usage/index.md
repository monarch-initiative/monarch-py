# Usage

monarch-py can be used via command line, or as a Python module.

## CLI

### Overview 

monarch-py can be used to query various implementations of the Monarch knowledge graph.  
The default implementation is Solr, and can optionally be omitted from the command,  
or an implementation can be specified as the first argument for `monarch`.  

For example:
```bash
# The following two commands are equivalent,
# as both query the Solr KG
$ monarch entity --id MONDO:0012933 
$ monarch solr entity --id MONDO:0012933

# Whereas the following specifies the SQL implementation
$ monarch sql entity --id MONDO:0012933
```

### Commands

```bash
$ monarch schema
```
╰ Print the linkml schema for the data model  

```bash
$ monarch [solr|sql] entity OPTIONS ARGS
```
╰ Retrieve an entity by ID  

| OPTIONS | | 
| --- | --- |
| `--update/-u` | Whether to re-download the Monarch KG |

| ARGUMENTS | | 
| --- | --- |
| `--id` | The identifier of the entity to be retrieve |

```bash
$ monarch [solr|sql] associations OPTIONS ARGS
```
╰ Paginate through associations 
    
| OPTIONS | | 
| --- | --- |
| `--update/-u` | Whether to re-download the Monarch KG |

| ARGUMENTS | | 
| --- | --- |
| `--category` | The category of the association |
| `--predicate` | The predicate of the association |
| `--subject` | The subject of the association |
| `--object` | The object of the association |
| `--entity` | The subject or object of the association |
| `--limit` | The number of associations to return |
| `--offset` | The offset of the first association to be retrieved |

```bash
monarch [solr] search OPTIONS ARGS
```
╰ Search for entities (Solr only)  
    
| OPTIONS | | 
| --- | --- |
| `--update/-u` | Whether to re-download the Monarch KG |

| ARGUMENTS | |
| --- | --- |
| `--query/-q` | The query string to search for |
| `--category` | The category of the entity |
| `--taxon` | The taxon of the entity |
| `--limit` | The number of entities to return |
| `--offset` | The offset of the first entity to be retrieved |

## Module

TBD