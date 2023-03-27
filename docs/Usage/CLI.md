# `monarch`

**Usage**:

```console
$ monarch [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `autocomplete`: Return entity autcomplete matches for a...
* `entity`: Retrieve an entity by ID
* `histopheno`: Retrieve the histopheno data for an entity...
* `schema`: Print the linkml schema for the data model
* `search`: Search for entities
* `solr`
* `sql`

## `monarch associations`

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
$ monarch associations [OPTIONS]
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

## `monarch autocomplete`

Return entity autcomplete matches for a query string

Args:
    q: The query string to autocomplete against
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ monarch autocomplete [OPTIONS] [Q]
```

**Arguments**:

* `[Q]`: Query string to autocomplete against

**Options**:

* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `monarch entity`

Retrieve an entity by ID

Args:
    id: The identifier of the entity to be retrieved
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ monarch entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `monarch histopheno`

Retrieve the histopheno data for an entity by ID

Args:
    subject: The subject of the association

Optional Args:
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ monarch histopheno [OPTIONS] [SUBJECT]
```

**Arguments**:

* `[SUBJECT]`: The subject of the association

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

## `monarch schema`

Print the linkml schema for the data model

**Usage**:

```console
$ monarch schema [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `monarch search`

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
$ monarch search [OPTIONS]
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

## `monarch solr`

**Usage**:

```console
$ monarch solr [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `autocomplete`: Return entity autcomplete matches for a...
* `entity`: Retrieve an entity by ID
* `histopheno`: Retrieve the histopheno associations for a...
* `search`: Search for entities
* `start`: Starts a local Solr container.
* `status`
* `stop`: Stops the local Solr container.

### `monarch solr associations`

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
$ monarch solr associations [OPTIONS]
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

### `monarch solr autocomplete`

Return entity autcomplete matches for a query string

Args:
    q: The query string to autocomplete against
    fmt: The format of the output (TSV, YAML, JSON)
    output: The path to the output file (stdout if not specified)

**Usage**:

```console
$ monarch solr autocomplete [OPTIONS] [Q]
```

**Arguments**:

* `[Q]`: Query string to autocomplete against

**Options**:

* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `monarch solr entity`

Retrieve an entity by ID

Args:
    id (str): The identifier of the entity to be retrieved

Optional Args:
    update (bool): = Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ monarch solr entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `monarch solr histopheno`

Retrieve the histopheno associations for a given subject

Args:
    subject (str): The subject of the association

Optional Args:
    update (bool): Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ monarch solr histopheno [OPTIONS] [SUBJECT]
```

**Arguments**:

* `[SUBJECT]`: The subject of the association

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.

### `monarch solr search`

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
$ monarch solr search [OPTIONS]
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

### `monarch solr start`

Starts a local Solr container.

**Usage**:

```console
$ monarch solr start [OPTIONS]
```

**Options**:

* `--update / --no-update`: [default: no-update]
* `--help`: Show this message and exit.

### `monarch solr status`

**Usage**:

```console
$ monarch solr status [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `monarch solr stop`

Stops the local Solr container.

**Usage**:

```console
$ monarch solr stop [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `monarch sql`

**Usage**:

```console
$ monarch sql [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `associations`: Paginate through associations
* `entity`: Retrieve an entity by ID

### `monarch sql associations`

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
$ monarch sql associations [OPTIONS]
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

### `monarch sql entity`

Retrieve an entity by ID

Args:
    id (str): The identifier of the entity to be retrieved
    update (bool): = Whether to re-download the Monarch KG. Default False
    fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
    output (str): The path to the output file. Default stdout

**Usage**:

```console
$ monarch sql entity [OPTIONS] [ID]
```

**Arguments**:

* `[ID]`: The identifier of the entity to be retrieved

**Options**:

* `-u, --update`: Whether to re-download the Monarch KG
* `-f, --format TEXT`: The format of the output (TSV, YAML, JSON)  [default: json]
* `-o, --output TEXT`: The path to the output file
* `--help`: Show this message and exit.
