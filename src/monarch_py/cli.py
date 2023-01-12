import importlib
import pathlib
import sys

import sh
import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation

SOLR_DATA = pathlib.Path(__file__).parent / "solr-data"

app = typer.Typer()
solr_app = typer.Typer()
app.add_typer(solr_app, name="solr")


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

# _out_bufsize=100
@solr_app.command("download")
def get_solr():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz", "-O", "/tmp/solr.tar.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SOLR_DATA)
    sh.tar("-zxf", "/tmp/solr.tar.gz", "-C", f"{SOLR_DATA}", _out=sys.stdout, _err=sys.stderr)
    sh.rm("/tmp/solr.tar.gz")

@solr_app.command("start")
def start_solr():
    data = pathlib.Path(f"{SOLR_DATA}/data")
    sh.docker.run("-p", "8983:8983", "-v", f"{data}:/opt", "-e", "SOLR_HOME=/opt/data", "--name", "monarch_solr","solr:8", _out=sys.stdout, _err=sys.stderr)

@solr_app.command("stop")
def stop_solr():
    sh.docker.stop("monarch_solr", _out=sys.stdout, _err=sys.stderr)
    sh.docker.rm("monarch_solr")

@solr_app.command("remove")
def delete_solr():
    sh.rm("-rf", SOLR_DATA)


if __name__ == "__main__":
    app()
