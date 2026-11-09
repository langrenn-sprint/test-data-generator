"""Test module for cli."""

from datetime import UTC, datetime
from pathlib import Path

from click.testing import CliRunner

from test_data_generator import cli


def season_offset() -> int:
    """Return 1 from August through December (season ends next year), else 0."""
    return 1 if datetime.now(tz=UTC).month >= 8 else 0


def expected_class_number(date_of_birth: str) -> int:
    """Return the class number for a 'dd.mm.yyyy' birthdate in the current season."""
    season_end_year = datetime.now(tz=UTC).year + season_offset()
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


def test_cli_with_no_value_for_number_of_rows(tmp_path: Path) -> None:
    """Should generate a test dataset with 1+100 lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(cli, ["-o", str(output_file)])
    assert result.exit_code == 0, result.output
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 101


def test_cli_with_value_for_number_of_rows(tmp_path: Path) -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(cli, ["-o", str(output_file), "-n", "10"])
    assert result.exit_code == 0, result.output
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 11


def test_cli_with_format_sportsadmin(tmp_path: Path) -> None:
    """Should generate a test dataset with 2 + 1 + default (100) number of lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(cli, ["-o", str(output_file), "-f", "Sportsadmin"])
    assert result.exit_code == 0, result.output
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 103


def test_cli_with_value_for_sex(tmp_path: Path) -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(cli, ["-o", str(output_file), "-n", "10", "--sex", "K"])
    assert result.exit_code == 0, result.output
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 11, result.output
    with output_file.open() as file:
        file.readline()  # Skip header
        for line in file:
            assert line.split(";")[9] == "K"


def test_cli_with_value_for_sex_and_age_women(tmp_path: Path) -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(
        cli,
        [
            "-o",
            str(output_file),
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
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 11
    with output_file.open() as file:
        file.readline()  # Skip header
        for line in file:
            assert line.split(";")[9] == "K"
            fields = line.split(";")
            birth_year = int(fields[8].split(".")[2])
            assert int(fields[7]) == datetime.now(tz=UTC).year - birth_year
            class_number = expected_class_number(fields[8])
            # Age 10 today means born in one of two years:
            assert class_number in {10 + season_offset(), 11 + season_offset()}
            assert fields[21] == f"Jenter {class_number}"


def test_cli_with_value_for_sex_and_age_men(tmp_path: Path) -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(
        cli,
        [
            "-o",
            str(output_file),
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
    with output_file.open() as file:
        num_lines = sum(1 for _ in file)
    assert num_lines == 11
    with output_file.open() as file:
        file.readline()  # Skip header
        for line in file:
            assert line.split(";")[9] == "M"
            fields = line.split(";")
            birth_year = int(fields[8].split(".")[2])
            assert int(fields[7]) == datetime.now(tz=UTC).year - birth_year
            class_number = expected_class_number(fields[8])
            # Age 17 today means born in one of two years:
            assert class_number in {17 + season_offset(), 18 + season_offset()}
            expected = f"Menn {class_number}" if class_number < 19 else "Menn 19-20"
            assert fields[21] == expected


def test_cli_with_format_sportsadmin_has_three_dummy_columns(tmp_path: Path) -> None:
    """Should write three columns with header 'Dummy', as in Sportsadmin exports."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(
        cli, ["-o", str(output_file), "--format", "Sportsadmin", "-n", "1"]
    )
    assert result.exit_code == 0, result.output
    with output_file.open() as file:
        lines = file.read().splitlines()
    header = lines[2].split(";")
    assert header.count("Dummy") == 3
    assert not any(column.startswith("Dummy-") for column in header)
    assert len(lines[3].split(";")) == len(header)


def test_cli_with_output_format_option(tmp_path: Path) -> None:
    """Should accept --output-format as well as the --format alias."""
    runner = CliRunner()
    output_file = tmp_path / "test.csv"
    result = runner.invoke(
        cli, ["-o", str(output_file), "--output-format", "iSonen", "-n", "1"]
    )
    assert result.exit_code == 0, result.output
    assert "Output format: iSonen" in result.output
