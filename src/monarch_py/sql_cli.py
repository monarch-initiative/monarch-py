from pathlib import Path
import sys

import sh
import typer

sql_app = typer.Typer()

SQL_DATA = Path(__file__).parent / "data" / "sql"

@sql_app.command("download")
def download_sql():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/monarch-kg.db.gz", "-O", "monarch-kg.db.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SQL_DATA)
    sh.gzip("-df", "monarch-kg.db.gz")
    sh.mv("monarch-kg.db", SQL_DATA)


@sql_app.command("remove")
def delete_sql():
    sh.rm('-rf', SQL_DATA)

