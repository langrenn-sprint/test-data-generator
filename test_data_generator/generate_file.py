"""Generate a test dataset (csv) with the given number of rows."""
import csv

from faker import Faker

from .providers.contestant_profile import ContestantProvider, SexLiteral

fake = Faker("no_NO")
fake.add_provider(ContestantProvider)

SPORTSADMIN_HEADER = '"Påmeldinger til KM Skagen Oslo Sprint 2022 08.01.2022 - 08.01.2022";;;;;;;;;;;;;;;;;;;;;;;;;;;\n'  # noqa: B950


def generate_file(
    file_name: str,
    format: str,
    number_of_rows: int,
    minimum_age: int,
    maximum_age: int,
    sex: SexLiteral,
) -> None:
    """Generate a test dataset (csv) with the given number of rows.

    Args:
        file_name (str): Name of the output file.
        format (str): Format of the output file.
        number_of_rows (int): Number of rows to generate.
        minimum_age (int): Minimum age of contestants.
        maximum_age (int): Maximum age of contestants.
        sex (SexLiteral): Sex of contestants.
    """
    # Extract column names and properties from format:
    columns = get_columns(format, minimum_age, maximum_age, sex)
    with open(file_name, "w", newline="", encoding="UTF-8") as file:
        if format == "sportsadmin":
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
                format=format, minimum_age=minimum_age, maximum_age=maximum_age, sex=sex
            )
            csvwriter.writerow(contestant.values())


def get_columns(
    format: str, minimum_age: int, maximum_age: int, sex: SexLiteral
) -> list[str]:
    """Get columns from format.

    Args:
        format (str): Format of the output file.
        minimum_age (int): Minimum age of contestants.
        maximum_age (int): Maximum age of contestants.
        sex (SexLiteral): Sex of contestants.

    Returns:
        list: List of columns.
    """
    _contestant = fake.contestant(
        format=format, minimum_age=minimum_age, maximum_age=maximum_age, sex=sex
    )
    columns = list(_contestant.keys())
    return columns
