"""Generate a test dataset (csv) with the given number of rows."""

import csv
import re
from pathlib import Path

from faker import Faker

from .providers.contestant_profile import ContestantProvider, SexLiteral

fake = Faker("no_NO")
fake.add_provider(ContestantProvider)

SPORTSADMIN_HEADER = '"Påmeldinger til KM Skagen Oslo Sprint 2022 08.01.2022 - 08.01.2022";;;;;;;;;;;;;;;;;;;;;;;;;;;\n'  # noqa: E501


def generate_file(  # noqa:PLR0917
    file_name: str,
    output_format: str,
    number_of_rows: int,
    minimum_age: int,
    maximum_age: int,
    sex: SexLiteral,
) -> None:
    """Generate a test dataset (csv) with the given number of rows.

    Args:
        file_name (str): Name of the output file.
        output_format (str): Format of the output file.
        number_of_rows (int): Number of rows to generate.
        minimum_age (int): Minimum age of contestants.
        maximum_age (int): Maximum age of contestants.
        sex (SexLiteral): Sex of contestants.
    """
    # Extract column names and properties from output_format:
    columns = get_columns(output_format, minimum_age, maximum_age, sex)
    with Path(file_name).open("w", newline="", encoding="UTF-8") as file:
        if output_format == "sportsadmin":
            file.write(SPORTSADMIN_HEADER)
            file.write(";;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
        # Write header
        csvwriter = csv.writer(
            file,
            delimiter=";",
            quoting=csv.QUOTE_NONE,
            escapechar="\\",
        )
        csvwriter.writerow(columns)

        # Generate and write rows:
        for _ in range(number_of_rows):
            contestant = fake.contestant(
                output_format=output_format,
                minimum_age=minimum_age,
                maximum_age=maximum_age,
                sex=sex,
            )
            csvwriter.writerow(contestant.values())


def get_columns(
    output_format: str, minimum_age: int, maximum_age: int, sex: SexLiteral
) -> list[str]:
    """Get columns from output_format.

    Args:
        output_format (str): Format of the output file.
        minimum_age (int): Minimum age of contestants.
        maximum_age (int): Maximum age of contestants.
        sex (SexLiteral): Sex of contestants.

    Returns:
        list: List of columns.
    """
    _contestant = fake.contestant(
        output_format=output_format,
        minimum_age=minimum_age,
        maximum_age=maximum_age,
        sex=sex,
    )
    # Dict keys must be unique, but some formats (e.g. Sportsadmin) have
    # several columns with the same header, e.g. "Dummy-1", "Dummy-2" -> "Dummy":
    return [re.sub(r"^(Dummy)-\d+$", r"\1", key) for key in _contestant]
