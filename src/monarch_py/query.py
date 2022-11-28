from dataclasses import dataclass
from urllib.parse import urlencode, urljoin


@dataclass
class SolrQuery:
    q: str = "*:*"
    offset: int = 0
    limit: int = 20
    category: str = None
    predicate: str = None
    subject: str = None
    object: str = None

    def get_args(self) -> dict:
        args = {k: v for (k, v) in self.__dict__.items() if v is not None}
        return args

    def build_query(self):  # , core=Union[Literal['entity'], Literal['association']]):
        pass  # query = f'?q={self.q}&offset={offset}'


@dataclass
class SolrEntityQuery(SolrQuery):
    pass


@dataclass
class SolrAssociationQuery(SolrQuery):
    entity: str = None  # return nodes where entity is subject or object
    between: str = None  # strip by comma and check associations in both directions. example: "MONDO:000747,MONDO:000420"


def build_query(args: dict):
    base_url = f"{solr_url}/association/query"
    query = "?" + urlencode(args)
    return urljoin(base_url, query)


def get_query_url(
    q: str = "*:*",
    offset: int = 0,
    limit: int = 20,
    category: str = None,
    predicate: str = None,
    subject: str = None,
    object: str = None,
    entity: str = None,  # return nodes where entity is subject or object
    between: str = None,  # strip by comma and check associations in both directions. example: "MONDO:000747,MONDO:000420"
) -> str:
    args = {k: v for (k, v) in locals().items() if v is not None}
    # Add logic to split q= and fq=
    # Add logic to deal with entity and between
    query = build_query(args)
    print(query)

    # if between:
    #     b = between.split(",")
    #     query += f'(subject:"{b[0]}" AND object:"{b[1]}") OR (subject:"{b[1]}" AND object:"{b[0]}")&'
    # if entity:
    #     query += f'subject:"{i}" OR object:"{i}"&'


def build_association_query(
    q: str = "*:*",
    offset: int = 0,
    limit: int = 20,
    category: str = None,
    predicate: str = None,
    subject: str = None,
    object: str = None,
    entity: str = None,  # return nodes where entity is subject or object
    between: str = None,  # strip by comma and check associations in both directions. example: "MONDO:000747,MONDO:000420"
) -> str:
    query = "?"
    query_params = [f"q={q}", f"offset={offset}", f"limit={limit}"]

    for i in query_params:
        query += f"{i}&"

    query += "fq="

    return query
