"""Main CLI for the transform step."""
import logging
from os import getenv

import click

from .generate_file import generate_file

logging.basicConfig(level=getenv("LOGGING_LEVEL", logging.INFO))


@click.command(name="test-data-generator")
@click.version_option()
@click.option("--outputfile", "-o", help="Output file name.", required=True)
@click.option(
    "--format",
    "-f",
    help="Output file format.",
    type=click.Choice(["Sportsadmin", "iSonen"], case_sensitive=False),
    default="iSonen",
)
@click.option(
    "--number_of_rows",
    "-n",
    help="Number of rows to generate.",
    type=int,
    default=100,
)
def cli(outputfile: str, format: str, number_of_rows) -> None:
    """CLI for generating test datasets (csv)."""
    click.echo(f"Output file: {outputfile}")
    click.echo(f"Output format: {format}")
    generate_file(outputfile, format, number_of_rows)
