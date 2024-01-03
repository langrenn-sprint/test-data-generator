"""Main CLI for the transform step."""
import logging
from os import getenv

import click

from .generate_file import generate_file
from .providers.contestant_profile import SexLiteral

logging.basicConfig(level=getenv("LOGGING_LEVEL", logging.INFO))


@click.command(name="test-data-generator")
@click.version_option()
@click.option("--outputfile", "-o", help="Output file name.", required=True)
@click.option(
    "--format",
    "-f",
    help="Output file format.",
    type=click.Choice(["Sportsadmin", "iSonen"], case_sensitive=False),
    required=True,
    default="iSonen",
    show_default=True,
)
@click.option(
    "--number_of_rows",
    "-n",
    help="Number of rows to generate.",
    type=int,
    default=100,
    show_default=True,
)
@click.option(
    "--minimum_age",
    "-min",
    help="Minimum age of contestants.",
    type=int,
    default=10,
    required=False,
    show_default=True,
)
@click.option(
    "--maximum_age",
    "-max",
    help="Maximum age of contestants.",
    type=int,
    default=22,
    required=False,
    show_default=True,
)
@click.option(
    "--sex",
    "-s",
    help="Sex of contenstants.",
    type=click.Choice([" ", "K", "M"], case_sensitive=False),
    default=" ",
    required=False,
    show_default=True,
)
def cli(
    outputfile: str,
    format: str,
    number_of_rows: int,
    minimum_age: int,
    maximum_age: int,
    sex: SexLiteral,
) -> None:
    """CLI for generating test datasets (csv)."""
    click.echo(f"Output file: {outputfile}")
    click.echo(f"Output format: {format}")
    # normalizes format:
    format = format.lower()
    generate_file(
        file_name=outputfile,
        format=format,
        number_of_rows=number_of_rows,
        minimum_age=minimum_age,
        maximum_age=maximum_age,
        sex=sex,
    )
