# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `entity`: Retrieve an entity by ID
* `histopheno`: Retrieve the histopheno data for an entity...
* `schema`: Print the linkml schema for the data model
* `search`: Search for entities
* `solr`
* `sql`

## `associations`

Paginate through associations

Args:
    category: The category of the association
    predicate: The predicate of the association
    subject: The subject of the association
    object: The object of the association
    entity: The subject or object of the association
    limit: The number of associations to return
    offset: The offset of the first association to be retrieved
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ associations [OPTIONS]
```

**Options**:

* `-c, --category TEXT`
* `-s, --subject TEXT`
* `-p, --predicate TEXT`
* `-o, --object TEXT`
* `-e, --entity TEXT`
* `--between TEXT`
* `-l, --limit INTEGER`: [default: 20]
* `--offset INTEGER`: [default: 0]
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `entity`

Retrieve an entity by ID

Args:
    id: The identifier of the entity to be retrieved
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `histopheno`

Retrieve the histopheno data for an entity by ID

Args:
    subject: The subject of the association

Optional Args:
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ histopheno [OPTIONS] [SUBJECT]
```

**Arguments**:

* `[SUBJECT]`: The subject of the association

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `schema`

Print the linkml schema for the data model

**Usage**:

```console
$ schema [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `search`

Search for entities

Args:
    q: The query string to search for
    category: The category of the entity
    taxon: The taxon of the entity
    limit: The number of entities to return
    offset: The offset of the first entity to be retrieved
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ search [OPTIONS]
```

**Options**:

* `-q, --query TEXT`
* `--category TEXT`
* `--taxon TEXT`
* `--limit INTEGER`: [default: 20]
* `--offset INTEGER`: [default: 0]
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `solr`

**Usage**:

```console
$ solr [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `entity`: Retrieve an entity by ID
* `histopheno`: Retrieve the histopheno associations for a...
* `remove`
* `search`: Search for entities
* `start`: Start a local Monarch Solr instance.
* `status`: Check the status of the local Monarch Solr...
* `stop`: Stop the local Monarch Solr instance.

### `solr associations`

Paginate through associations

Args:
    category (str, optional): The category of the association.
    subject (str, optional): The subject of the association.
    predicate (str, optional): The predicate of the association.
    object (str, optional): The object of the association.
    entity (str, optional): The subject or object of the association.
    between (str, optional): Two comma-separated entities to get bi-directional associations.
    limit (int, optional): The number of associations to return. Default 20
    offset (int, optional): The offset of the first association to be retrieved. Default 0
    update (bool, optional): Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ solr associations [OPTIONS]
```

**Options**:

* `--category TEXT`
* `--subject TEXT`
* `--predicate TEXT`
* `--object TEXT`
* `--entity TEXT`
* `--between TEXT`
* `--limit INTEGER`: [default: 20]
* `--offset INTEGER`: [default: 0]
* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `solr entity`

Retrieve an entity by ID

Args:
    id (str): The identifier of the entity to be retrieved

Optional Args:
    update (bool): = Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ solr entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `solr histopheno`

Retrieve the histopheno associations for a given subject

Args:
    subject (str): The subject of the association

Optional Args:
    update (bool): Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ solr histopheno [OPTIONS] [SUBJECT]
```

**Arguments**:

* `[SUBJECT]`: The subject of the association

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `solr remove`

**Usage**:

```console
$ solr remove [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `solr search`

Search for entities

Optional Args:
    q: The query string to search for
    category: The category of the entity
    taxon: The taxon of the entity
    limit: The number of entities to return
    offset: The offset of the first entity to be retrieved
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ solr search [OPTIONS]
```

**Options**:

* `-q, --query TEXT`
* `-c, --category TEXT`
* `-t, --taxon TEXT`
* `-l, --limit INTEGER`: [default: 20]
* `--offset INTEGER`: [default: 0]
* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `solr start`

Start a local Monarch Solr instance.

**Usage**:

```console
$ solr start [OPTIONS]
```

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG.
* `--help`: Show this message and exit.

### `solr status`

Check the status of the local Monarch Solr instance.

**Usage**:

```console
$ solr status [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `solr stop`

Stop the local Monarch Solr instance.

**Usage**:

```console
$ solr stop [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `sql`

**Usage**:

```console
$ sql [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `entity`: Retrieve an entity by ID

### `sql associations`

Paginate through associations

Args:
    category (str, optional): The category of the association.
    subject (str, optional): The subject of the association.
    predicate (str, optional): The predicate of the association.
    object (str, optional): The object of the association.
    entity (str, optional): The subject or object of the association.
    between (str, optional): Two comma-separated entities to get bi-directional associations.
    limit (int, optional): The number of associations to return. Default 20
    offset (int, optional): The offset of the first association to be retrieved. Default 0
    update (bool, optional): Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ sql associations [OPTIONS]
```

**Options**:

* `--category TEXT`
* `--subject TEXT`
* `--predicate TEXT`
* `--object TEXT`
* `--entity TEXT`
* `--between TEXT`
* `--limit INTEGER`: [default: 20]
* `--offset INTEGER`: [default: 0]
* `--update`
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `sql entity`

Retrieve an entity by ID

Args:
    id (str): The identifier of the entity to be retrieved
    update (bool): = Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ sql entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

