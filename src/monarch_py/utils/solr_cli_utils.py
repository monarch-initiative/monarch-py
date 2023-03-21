import os
import sys
import time

import docker
import pystow

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.utils.utils import SOLR_DATA_URL, console

monarchstow = pystow.module("monarch")
dc = docker.from_env()


def check_solr_permissions(update: bool = False) -> None:
    """Checks that the solr data directory has the correct permissions."""
    monarchstow.ensure_untar(url=SOLR_DATA_URL, force=update)
    if sys.platform in ["linux", "linux2", "darwin"]:
        stat_info = os.stat(monarchstow.base / "solr" / "data")
        if stat_info.st_gid != 8983:
            console.print(
                f"""
Solr container requires write access to {monarchstow.base}.
Please run the following command to set permissions:
    [grey84 on black]sudo chgrp -R 8983 {monarchstow.base}[/]
    [grey84 on black]sudo chmod -R g+w {monarchstow.base}[/]
            """
            )
            sys.exit(1)


def check_for_solr(quiet: bool = False):
    if not quiet:
        console.print("\nChecking for Solr container...")
    c = dc.containers.list(all=True, filters={"name": "monarch_solr"})
    return None if not c else c[0]


def get_solr(update: bool = False):
    """Checks for Solr data and container, and returns a SolrImplementation."""
    check_solr_permissions(update)
    if check_for_solr(quiet=True):
        return SolrImplementation()
    else:
        console.print(
            "\nNo Solr container found!\nStart a Solr container with [bold]monarch solr start[/]."
        )
        sys.exit(1)


def start_solr():
    """Starts a local Solr container."""
    data = monarchstow.join("solr", "data")
    c = check_for_solr(quiet=True)
    if not c:
        try:
            c = dc.containers.run(
                "solr:8",
                ports={"8983": 8983},
                volumes=[f"{data}:/opt/solr-data"],
                environment=["SOLR_HOME=/opt/solr-data"],
                name="monarch_solr",
                command="",
                detach=True,
            )
            time.sleep(10)
            console.print(f"{c.name} {c.status}")
        except Exception as e:
            console.print(f"Error instantiating monarch solr container: {e}")
            raise e
    else:
        try:
            c.start()
        except Exception as e:
            console.print(
                f"Error running existing container {c.name} ({c.status}) - {e}"
            )
            raise e


def stop_solr():
    """Stops the local Solr container."""
    c = check_for_solr(quiet=True)
    if c:
        try:
            console.print(f"Stopping {c.name}...")
            c.stop()
            c.remove()
        except Exception as e:
            console.print(f"Error stopping container {c.name} ({c.status}) - {e}")
            raise e


def solr_status():
    c = check_for_solr()
    if not c:
        console.print(
            """
No monarch_solr container found. 

Download the Monarch Solr KG and start a local solr instance:
    [grey84 on black]monarch solr start[/]
"""
        )
    else:
        console.print(
            f"""
Found monarch_solr container: {c.id}
Container status: {c.status}
        """
        )
        if c.status == "exited":
            console.print(
                """
Start the container using:
    [grey84 on black]monarch solr start[/]
"""
            )
        if c.status == "running":
            console.print(
                """
You can create a new container with
    [grey84 on black]monarch solr stop[/]
    [grey84 on black]monarch solr start[/]
"""
            )
