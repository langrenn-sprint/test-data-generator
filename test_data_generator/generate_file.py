"""Generate a test dataset (csv) with the given number of rows."""
import csv

from faker import Faker


def generate_file(file_name: str, format: str, number_of_rows: int) -> None:
    """Generate a test dataset (csv) with the given number of rows.

    Args:
        file_name (str): Name of the output file.
        format (str): Format of the output file.
        number_of_rows (int): Number of rows to generate.
    """
    # TODO: Add support for both formats.
    columns = [
        "first_name",
        "last_name",
        "date_of_birth",
        "email",
        "phone_number",
    ]
    with open(file_name, "w", newline="", encoding="UTF-8") as file:
        csvwriter = csv.writer(
            file,
            delimiter=";",
            quoting=csv.QUOTE_NONE,
            escapechar="\\",
        )
        csvwriter.writerow(columns)

        for _ in range(number_of_rows):
            fake = Faker("no_NO")
            csvwriter.writerow(
                [
                    fake.first_name(),
                    fake.last_name(),
                    fake.date_of_birth(minimum_age=9, maximum_age=80),
                    fake.email(),
                    fake.phone_number(),
                ]
            )
