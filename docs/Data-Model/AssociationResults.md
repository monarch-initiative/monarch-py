# Class: AssociationResults



URI: [https://w3id.org/monarch/monarch-py/:AssociationResults](https://w3id.org/monarch/monarch-py/:AssociationResults)



```mermaid
 classDiagram
    class AssociationResults
      Results <|-- AssociationResults
      
      AssociationResults : associations
      AssociationResults : limit
      AssociationResults : offset
      AssociationResults : total
      
```





## Inheritance
* [Results](Results.md)
    * **AssociationResults**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [associations](associations.md) | 0..* <br/> [Association](Association.md) |  | direct |
| [limit](limit.md) | 0..1 <br/> [xsd:integer](xsd:integer) |  | [Results](Results.md) |
| [offset](offset.md) | 0..1 <br/> [xsd:integer](xsd:integer) |  | [Results](Results.md) |
| [total](total.md) | 0..1 <br/> [xsd:integer](xsd:integer) |  | [Results](Results.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/monarch/monarch-py





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/monarch/monarch-py/:AssociationResults |
| native | https://w3id.org/monarch/monarch-py/:AssociationResults |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: AssociationResults
from_schema: https://w3id.org/monarch/monarch-py
rank: 1000
is_a: Results
slots:
- associations

```
</details>

### Induced

<details>
```yaml
name: AssociationResults
from_schema: https://w3id.org/monarch/monarch-py
rank: 1000
is_a: Results
attributes:
  associations:
    name: associations
    from_schema: https://w3id.org/monarch/monarch-py
    rank: 1000
    multivalued: true
    alias: associations
    owner: AssociationResults
    domain_of:
    - AssociationResults
    range: Association
    inlined: true
    inlined_as_list: true
  limit:
    name: limit
    from_schema: https://w3id.org/monarch/monarch-py
    rank: 1000
    alias: limit
    owner: AssociationResults
    domain_of:
    - Results
    range: integer
  offset:
    name: offset
    from_schema: https://w3id.org/monarch/monarch-py
    rank: 1000
    alias: offset
    owner: AssociationResults
    domain_of:
    - Results
    range: integer
  total:
    name: total
    from_schema: https://w3id.org/monarch/monarch-py
    rank: 1000
    alias: total
    owner: AssociationResults
    domain_of:
    - Results
    range: integer

```
</details>