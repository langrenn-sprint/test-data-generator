"""Module for custom provider contestant_profile."""

from datetime import UTC, date, datetime
from typing import Literal

from faker import Faker
from faker.providers import BaseProvider

SexLiteral = Literal["K", "M"]


class ContestantProvider(BaseProvider):
    """This provider is a collection of functions to generate personal profiles and identities."""  # noqa: E501

    def contestant(
        self,
        output_format: str,
        minimum_age: int,
        maximum_age: int,
        sex: SexLiteral | None = None,
    ) -> dict[str, int | str | date | SexLiteral]:
        """Creates a contestant-profile.

        Args:
            output_format (str): the output format of the resulting contestant
            minimum_age (int): the minimum age of the contestant
            maximum_age (int): the maximum age of the contestant
            sex (SexLiteral): the sex of the contestant ('K' or 'M')

        Returns:
            Dict[str, Union[int, str, date, SexLiteral]]: a contestant dictionary
        """
        date_of_birth_ = self.generator.date_of_birth(
            tzinfo=UTC, minimum_age=minimum_age, maximum_age=maximum_age
        )

        # if sex is empty, assign a random value:
        sex_: SexLiteral

        sex_ = sex if sex in {"K", "M"} else self.random_element(["K", "M"])

        if sex_ == "K":
            first_name = self.generator.first_name_female()
            last_name = self.generator.last_name_female()
        else:
            first_name = self.generator.first_name_male()
            last_name = self.generator.last_name_male()

        age_class_ = calculate_age_class(
            output_format=output_format,
            sex=sex_,
            date_of_birth=date_of_birth_,
            today=datetime.now(tz=UTC).date(),
        )
        club_ = self.random_element(list_of_clubs)

        if output_format.lower() == "isonen":
            return self.contestant_isonen(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth_,
                sex=sex_,
                age_class=age_class_,
                club=club_,
            )
        # sportsadmin
        return self.contestant_sportsadmin(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth_,
            sex=sex_,
            age_class=age_class_,
            club=club_,
        )

    def contestant_isonen(  # noqa:PLR0917
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        sex: SexLiteral,
        club: dict[str, str | int],
        age_class: str,
    ) -> dict[str, int | str | date | SexLiteral]:
        """Generates a basic profile with personal informations.

        Args:
            first_name (str): the first name of the contestant
            last_name (str): the last name of the contestant
            date_of_birth (date): the birthdate of the contestant
            sex (SexLiteral): the sex of the contestant
            club (dict[str, str1|int]): the club of the contestant
            age_class (str): the age class of the contestant

        Returns:
            Dict[str, Union[int, str, date, SexLiteral]]: a contestant dictionary
        """
        return {
            "Fornavn": first_name,
            "Etternavn": last_name,
            "E-post": self.generator.email(),
            "Mobil": self.generator.phone_number(),
            "Adresse": self.generator.street_address(),
            "Postnummer": self.generator.postcode(),
            "Sted": self.generator.city(),
            "Alder": datetime.now(tz=UTC).year - date_of_birth.year,
            "Fødselsdato": date_of_birth.strftime("%d.%m.%Y"),
            "Kjønn": sex,
            "Land": self.generator.current_country(),
            "Landskode": self.generator.current_country_code(),
            "Bypass ID": self.random_number(digits=9, fix_len=True),
            "Person ID": self.random_number(digits=7, fix_len=True),
            "Klubb": club["name"],
            "Klubb-ID": club["id"],
            "Gruppe-ID": self.random_number(digits=5, fix_len=True),
            "Krets/region-id": self.random_number(digits=3, fix_len=True),
            "Krets/region": "Oslo Skikrets",
            "Sport": "Ski",
            "Øvelse": "",
            "Klasse": age_class,
            "Team": "",
            "Påmeldt dato": self.generator.date_this_year(
                before_today=True, after_today=False
            ).strftime("%d.%m.%Y"),
            "Påmeldt kl.": self.generator.time_object().strftime("%H:%M"),
        }

    def contestant_sportsadmin(  # noqa:PLR0917
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        sex: SexLiteral,
        club: dict[str, str | int],
        age_class: str,
    ) -> dict[str, int | str | date | SexLiteral]:
        """Generates a basic profile with personal informations.

        Args:
            first_name (str): the first name of the contestant
            last_name (str): the last name of the contestant
            date_of_birth (date): the birthdate of the contestant
            sex (SexLiteral): the sex of the contestant
            club (dict[str, str|int]): the club of the contestant
            age_class (str): the age class of the contestant

        Returns:
            Dict[str, Union[int, str, date, SexLiteral]]: a contestant dictionary
        """
        return {
            "Klasse": age_class,
            "Øvelse": "sprint klassisk",
            "Dato": datetime.now(tz=UTC).strftime("%d.%m.%Y"),
            "Kl.": "800",
            "Etternavn": last_name,
            "Fornavn": first_name,
            "Kjønn": sex,
            "Fødselsdato": date_of_birth,
            "Idrettsnr": self.random_number(digits=7, fix_len=True),
            "E-post": self.generator.email(),
            "Org.tilhørighet": club["name"],
            "Krets/region": "Oslo Skikrets",
            "Brikkenummer": self.random_number(digits=9, fix_len=True),
            "Team": "",
            "Idrettsgymnas": "",
            "Stafettlag": "",
            "Etappe": "",
            "Lagleder": "",
            "Mobil lagleder": "",
            "E-post lagleder": "",
            "Dummy-1": "",
            "Dummy-2": "",
            "Dummy-3": "",
            "Betalt/påmeldt dato": self.generator.date_time_this_year(
                before_now=True, after_now=False
            ).strftime("%d.%m.%Y %H:%M:%S"),
            "Påmeldt av": self.generator.name(),
            "Tlf påmelder": self.generator.phone_number(),
            "E-post påmelder": self.generator.email(),
        }


# The skiing season starts in August and ends in July the following year.
SEASON_START_MONTH = 8


def calculate_age_class(  # noqa: C901
    output_format: str,
    sex: SexLiteral,
    date_of_birth: date,
    today: date,
) -> str:
    """Calculates age-class based on sex, date of birth and the current season.

    The skiing season runs from August through July. A contestant competes in the
    class equal to the age they reach in the calendar year the season ends. E.g. a
    contestant born in 2017 competes in class 10 from August 2026 to July 2027.

    Args:
        output_format (str): the output format of the resulting contestant
        sex (SexLiteral): the sex of the contestant ('K' or 'M')
        date_of_birth (date): the birthdate of the contestant
        today (date): the reference date, determines the current season

    Returns:
        str: the age-class of the contestant
    """
    season_end_year = (
        today.year + 1 if today.month >= SEASON_START_MONTH else today.year
    )
    age_class = season_end_year - date_of_birth.year

    if output_format == "sportsadmin":
        if age_class < 17:
            if sex == "K":
                return f"J {age_class} år"
            return f"G {age_class} år"
        if age_class < 19:
            if sex == "K":
                return f"K {age_class} år"
            return f"M {age_class} år"
        if age_class < 21:
            if sex == "K":
                return "K 19/20 år"
            return "M 19/20 år"
        if sex == "K":
            return "Kvinner senior"
        return "Menn senior"
    if age_class < 17:
        if sex == "K":
            return f"Jenter {age_class}"
        return f"Gutter {age_class}"
    if age_class < 19:
        if sex == "K":
            return f"Kvinner {age_class}"
        return f"Menn {age_class}"
    if age_class < 21:
        if sex == "K":
            return "Kvinner 19-20"
        return "Menn 19-20"
    if sex == "K":
        return "Kvinner senior"
    return "Menn senior"


# Create a list of clubs in Oslo:
list_of_clubs = [
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Bækkelagets SK - Ski",
    },
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Koll, IL - Ski"},
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Lyn Ski - Ski"},
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Kjelsås IL - Ski"},
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Idrettslaget Try - Ski",
    },
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Røa Allianseidrettslag - Ski",
    },
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Rustad Idrettslag - Ski",
    },
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Årvoll IL - Ski"},
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Hasle-Løren IL - Ski",
    },
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Heming, IL - Ski"},
    {
        "id": Faker().random_number(digits=5, fix_len=True),
        "name": "Lillomarka Skiklubb - Ski",
    },
    {"id": Faker().random_number(digits=5, fix_len=True), "name": "Njård - Ski"},
]
