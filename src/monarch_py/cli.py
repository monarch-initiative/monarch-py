import importlib
import pathlib

import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation

app = typer.Typer()


@app.command()
def schema():
    """
    Print the linkml schema for the data model
    """
    schema_name = "model"
    schema_dir = pathlib.Path(
        importlib.util.find_spec(f"monarch_py.datamodels.{schema_name}").origin
    ).parent
    schema_path = schema_dir / pathlib.Path(schema_name + ".yaml")
    with open(schema_path, "r") as schema_file:
        print(schema_file.read())


@app.command()
def entity(id: str):
    """
    Retrieve an entity by ID

    Args:
        id: The identifier of the entity to be retrieved

    """
    si = SolrImplementation()

    entity = si.get_entity(id)
    print(entity.json(indent=4))


@app.command()
def associations(
    category: str = typer.Option(None, "--category", "-c"),
    subject: str = typer.Option(None, "--subject", "-s"),
    predicate: str = typer.Option(None, "--predicate", "-p"),
    object: str = typer.Option(None, "--object", "-o"),
    entity: str = typer.Option(None, "--entity", "-e"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    # todo: add output_type as an option to support tsv, json, etc. Maybe also rich-cli tables?
):
    """
    Paginate through associations

    Args:
        category: The category of the association
        predicate: The predicate of the association
        subject: The subject of the association
        object: The object of the association
        entity: The subject or object of the association
        limit: The number of associations to return
        offset: The offset of the first association to be retrieved
    """
    si = SolrImplementation()

    response = si.get_associations(
        category=category,
        predicate=predicate,
        subject=subject,
        object=object,
        entity=entity,
        limit=limit,
        offset=offset,
    )

    print(response.json(indent=4))


if __name__ == "__main__":
    app()
