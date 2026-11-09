"""Test module for cli."""

import tempfile
from datetime import UTC, datetime
from pathlib import Path

from click.testing import CliRunner

from test_data_generator import cli


def expected_class_number(date_of_birth: str) -> int:
    """Return the class number for a 'dd.mm.yyyy' birthdate in the current season."""
    today = datetime.now(tz=UTC).date()
    season_end_year = today.year + 1 if today.month >= 8 else today.year
    return season_end_year - int(date_of_birth.split(".")[2])


def test_cli_with_no_arguments_or_options() -> None:
    """Should return the help message."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 2, result.output
    assert "Usage: test-data-generator [OPTIONS]" in result.output
    assert "Error: Missing option '--outputfile' / '-o'." in result.output


def test_cli_with_no_help_option() -> None:
    """Should return the help message."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Usage: test-data-generator [OPTIONS]" in result.output


def test_cli_with_version_option() -> None:
    """Should return the version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0, result.output
    assert "test-data-generator, version" in result.output


def test_cli_with_no_value_for_number_of_rows() -> None:
    """Should generate a test dataset with 1+100 lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(cli, ["-o", "test.csv"])
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 101


def test_cli_with_value_for_number_of_rows() -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(cli, ["-o", "test.csv", "-n", "10"])
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 11


def test_cli_with_format_sportsadmin() -> None:
    """Should generate a test dataset with 2 + 1 + default (100) number of lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(cli, ["-o", "test.csv", "-f", "Sportsadmin"])
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 103


def test_cli_with_value_for_sex() -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(cli, ["-o", "test.csv", "-n", "10", "--sex", "K"])
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 11, result.output
        with Path("test.csv").open() as file:
            file.readline()  # Skip header
            for line in file:
                assert line.split(";")[9] == "K"


def test_cli_with_value_for_sex_and_age_women() -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(
            cli,
            [
                "-o",
                "test.csv",
                "-n",
                "10",
                "--sex",
                "K",
                "--minimum_age",
                "10",
                "--maximum_age",
                "10",
            ],
        )
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 11
        with Path("test.csv").open() as file:
            file.readline()  # Skip header
            for line in file:
                assert line.split(";")[9] == "K"
                fields = line.split(";")
                birth_year = int(fields[8].split(".")[2])
                assert int(fields[7]) == datetime.now(tz=UTC).year - birth_year
                class_number = expected_class_number(fields[8])
                assert class_number in {11, 12}
                assert fields[21] == f"Jenter {class_number}"


def test_cli_with_value_for_sex_and_age_men() -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory():
        result = runner.invoke(
            cli,
            [
                "-o",
                "test.csv",
                "-n",
                "10",
                "--sex",
                "M",
                "--minimum_age",
                "17",
                "--maximum_age",
                "17",
            ],
        )
        assert result.exit_code == 0, result.output
        with Path("test.csv").open() as file:
            num_lines = sum(1 for _ in file)
        assert num_lines == 11
        with Path("test.csv").open() as file:
            file.readline()  # Skip header
            for line in file:
                assert line.split(";")[9] == "M"
                fields = line.split(";")
                birth_year = int(fields[8].split(".")[2])
                assert int(fields[7]) == datetime.now(tz=UTC).year - birth_year
                class_number = expected_class_number(fields[8])
                assert class_number in {18, 19}
                expected = "Menn 18" if class_number == 18 else "Menn 19-20"
                assert fields[21] == expected
