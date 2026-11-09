"""Test module for calculate_age_class."""

from datetime import date

import pytest

from test_data_generator.providers.contestant_profile import (
    SexLiteral,
    calculate_age_class,
)

BORN_2017 = date(2017, 5, 17)


# Season boundaries:
@pytest.mark.parametrize(
    ("today", "expected"),
    [
        (date(2026, 7, 31), "Jenter 9"),  # last day of season 2025/2026
        (date(2026, 8, 1), "Jenter 10"),  # first day of season 2026/2027
        (date(2026, 12, 31), "Jenter 10"),
        (date(2027, 1, 1), "Jenter 10"),
        (date(2027, 7, 31), "Jenter 10"),  # last day of season 2026/2027
        (date(2027, 8, 1), "Jenter 11"),  # first day of season 2027/2028
    ],
)
def test_calculate_age_class_follows_season(today: date, expected: str) -> None:
    """Class should be the age reached in the year the season (Aug-Jul) ends."""
    assert (
        calculate_age_class(
            output_format="isonen", sex="K", date_of_birth=BORN_2017, today=today
        )
        == expected
    )


def test_calculate_age_class_ignores_day_of_birth() -> None:
    """Contestants born the same year should be in the same class."""
    today = date(2026, 11, 9)
    first = calculate_age_class(
        output_format="isonen", sex="K", date_of_birth=date(2017, 1, 1), today=today
    )
    last = calculate_age_class(
        output_format="isonen", sex="K", date_of_birth=date(2017, 12, 31), today=today
    )
    assert first == last == "Jenter 10"


# Sportsadmin:
@pytest.mark.parametrize(
    ("sex", "born", "expected"),
    [
        ("K", 2017, "J 10 år"),
        ("M", 2017, "G 10 år"),
        ("K", 2010, "K 17 år"),
        ("M", 2009, "M 18 år"),
        ("K", 2008, "K 19/20 år"),
        ("M", 2007, "M 19/20 år"),
        ("K", 2006, "Kvinner senior"),
        ("M", 2006, "Menn senior"),
    ],
)
def test_calculate_age_class_sportsadmin(
    sex: SexLiteral, born: int, expected: str
) -> None:
    """Should return Sportsadmin class names in season 2026/2027."""
    assert (
        calculate_age_class(
            output_format="sportsadmin",
            sex=sex,
            date_of_birth=date(born, 3, 1),
            today=date(2026, 11, 9),
        )
        == expected
    )


# iSonen:
@pytest.mark.parametrize(
    ("sex", "born", "expected"),
    [
        ("K", 2017, "Jenter 10"),
        ("M", 2017, "Gutter 10"),
        ("K", 2010, "Kvinner 17"),
        ("M", 2009, "Menn 18"),
        ("K", 2008, "Kvinner 19-20"),
        ("M", 2007, "Menn 19-20"),
        ("K", 2006, "Kvinner senior"),
        ("M", 2006, "Menn senior"),
    ],
)
def test_calculate_age_class_isonen(sex: SexLiteral, born: int, expected: str) -> None:
    """Should return iSonen class names in season 2026/2027."""
    assert (
        calculate_age_class(
            output_format="isonen",
            sex=sex,
            date_of_birth=date(born, 3, 1),
            today=date(2026, 11, 9),
        )
        == expected
    )
