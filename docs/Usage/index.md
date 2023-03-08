# Usage

monarch-py can be used via command line, or as a Python module.

## CLI

### Overview 

monarch-py can be used to query various implementations of the Monarch knowledge graph.  
The default, and more feature-rich, implementation is Solr, and is the default.

Subcommands are available to specify the backend.

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

CLI commands are listed [here](./CLI.md), or can be found by running `monarch --help`.

## Module

TBD