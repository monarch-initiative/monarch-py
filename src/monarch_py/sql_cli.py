from pathlib import Path
import sys

import sh
import typer

from monarch_py.implementations.sql.sql_implementation import SQLImplementation
from monarch_py.utilities.utils import check_for_data

sql_app = typer.Typer()

SQL_DATA = Path(__file__).parent / "data" / "sql"


def get_sql():
    if not check_for_data('sql'):
        cont = typer.confirm(f"\nSQL database not found locally. Would you like to download?\n")
        if not cont:
            print("Please download the Monarch KG before proceeding.")
            typer.Abort()
        download_sql()
    return SQLImplementation()


@sql_app.command("download")
def download_sql():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/monarch-kg.db.gz", "-O", "monarch-kg.db.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SQL_DATA)
    sh.gzip("-df", "monarch-kg.db.gz")
    sh.mv("monarch-kg.db", SQL_DATA)


@sql_app.command("remove")
def delete_sql():
    sh.rm('-rf', SQL_DATA)


@sql_app.command()
def entity(id: str = typer.Option(None, "--id")):
    """
    Retrieve an entity by ID

    Args:
        input: Which KG to use - solr or sql
        id: The identifier of the entity to be retrieved

    """
    data = get_sql()
    entity = data.get_entity(id)
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
        between: Two comma-separated entities to get bi-directional associations
        limit: The number of associations to return
        offset: The offset of the first association to be retrieved
    """
    args = locals()
    data = get_sql()
    response = data.get_associations(**args)
    print(response.json(indent=4))

