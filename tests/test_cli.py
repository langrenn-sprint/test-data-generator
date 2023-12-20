"""Test module for cli."""
from click.testing import CliRunner
from test_data_generator import cli


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
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["-o", "test.csv"])
        assert result.exit_code == 0, result.output
        num_lines = sum(1 for _ in open("test.csv"))
        assert num_lines == 101, result.output


def test_cli_with_value_for_number_of_rows() -> None:
    """Should generate a test dataset with 1 + given number of lines."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["-o", "test.csv", "-n", "10"])
        assert result.exit_code == 0, result.output
        num_lines = sum(1 for _ in open("test.csv"))
        assert num_lines == 11, result.output
