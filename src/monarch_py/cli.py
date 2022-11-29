import importlib
import pathlib

import typer

from monarch_py.implementations.solr.solr_implentation import SolrImplementation

app = typer.Typer()


@app.command()
def schema():
    """
    This method prints the linkml schema to stdout, so that downstream tools can extend the schema as necessary
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
    This is just a stub / placeholder / proof of concept of printing an entity to stdout

    Args:
        id: The identifier of the entity to be retrieved

    """
    si = SolrImplementation()

    entity = si.get_entity(id)
    print(entity.json(indent=4))


if __name__ == "__main__":
    app()
