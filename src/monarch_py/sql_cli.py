from pathlib import Path
import sys

import sh
import typer

sql_app = typer.Typer()

SQL_DATA = Path(__file__).parent / "data" / "sql"

@sql_app.command("download")
def get_sql():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/monarch-kg.db.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SQL_DATA)
    sh.tar("-zxf", "monarch-kg.db.gz", "-C", f"{SQL_DATA}", _out=sys.stdout, _err=sys.stderr)
    sh.rm("monarch-kg.db.gz")


@sql_app.command()
def delete_sql():
    sh.rm('-rf', SQL_DATA)

