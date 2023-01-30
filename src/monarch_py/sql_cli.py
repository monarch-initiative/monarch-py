import typer

from monarch_py.implementations.sql.sql_implementation import SQLImplementation

sql_app = typer.Typer()


@sql_app.command()
def entity(
    id: str = typer.Option(None, "--id", help="The identifier of the entity to be retrieved"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG")
    ):
    """Retrieve an entity by ID

    Args:
        id (str): The identifier of the entity to be retrieved
        update (bool): = Whether to re-download the Monarch KG. Default False
    """
    data = SQLImplementation()
    entity = data.get_entity(id, update)
    if not entity:
        print(f"\nEntity '{id}' not found.\n")
        typer.Abort()
    else:
        print(entity.json(indent=4))

    

@sql_app.command()
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    update: bool = typer.Option(False, "--update"),
    # todo: add output_type as an option to support tsv, json, etc. Maybe also rich-cli tables?
    ):
    """Paginate through associations

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
    """
    args = locals()
    data = SQLImplementation()
    response = data.get_associations(**args)
    print(response.json(indent=4))

