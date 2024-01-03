"""Module for custom provider contestant_profile."""
from datetime import date, datetime
from typing import Dict, Literal, Optional, Union

from faker import Faker
from faker.providers import BaseProvider

SexLiteral = Literal["K", "M"]


class ContestantProvider(BaseProvider):
    """This provider is a collection of functions to generate personal profiles and identities."""

    def contestant(
        self,
        format: str,
        minimum_age: int,
        maximum_age: int,
        sex: Optional[SexLiteral] = None,
    ) -> Dict[str, Union[int, str, date, SexLiteral]]:
        """Creates a contestant-profile.

        Args:
            format (str): the format of the resulting contestant
            minimum_age (int): the minimum age of the contestant
            maximum_age (int): the maximum age of the contestant
            sex (SexLiteral): the sex of the contestant ('K' or 'M')

        Returns:
            Dict[str, Union[int, str, date, SexLiteral]]: a contestant dictionary
        """
        date_of_birth_ = self.generator.date_of_birth(
            tzinfo=None, minimum_age=minimum_age, maximum_age=maximum_age
        )
        age_ = date.today().year - date_of_birth_.year
        # if sex is empty, assign a radnom value:
        sex_: SexLiteral
        if sex == "K" or sex == "M":
            sex_ = sex
        else:
            sex_ = self.random_element(["K", "M"])

        if sex_ == "K":
            first_name = self.generator.first_name_female()
            last_name = self.generator.last_name_female()
        elif sex_ == "M":
            first_name = self.generator.first_name_male()
            last_name = self.generator.last_name_male()
        age_class_ = calculate_age_class(format=format, sex=sex_, age=age_)
        club_ = self.random_element(list_of_clubs)

        if format.lower() == "isonen":
            return self.contestant_isonen(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth_,
                sex=sex_,
                age_class=age_class_,
                club=club_,
            )
        else:  # sportsadmin
            return self.contestant_sportsadmin(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth_,
                sex=sex_,
                age_class=age_class_,
                club=club_,
            )

    def contestant_isonen(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        sex: SexLiteral,
        club: dict[str, Union[str, int]],
        age_class: str,
    ) -> Dict[str, Union[int, str, date, SexLiteral]]:
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
            "Alder": date.today().year - date_of_birth.year,
            "Fødselsdato": date_of_birth,
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
            "Øvelse": age_class,
            "Klasse": "",
            "Team": "",
            "Påmeldt dato": self.generator.date_this_year(
                before_today=True, after_today=False
            ).strftime("%d.%m.%Y"),
            "Påmeldt kl.": self.generator.time_object().strftime("%H:%M"),
        }

    def contestant_sportsadmin(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        sex: SexLiteral,
        club: dict[str, Union[str, int]],
        age_class: str,
    ) -> Dict[str, Union[int, str, date, SexLiteral]]:
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
            "Dato": datetime.today().strftime("%d.%m.%Y"),
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
            "Dummy": "",
            "Dummy": "",
            "Dummy": "",
            "Betalt/påmeldt dato": self.generator.date_time_this_year(
                before_now=True, after_now=False
            ).strftime("%d.%m.%Y %H:%M:%S"),
            "Påmeldt av": self.generator.name(),
            "Tlf påmelder": self.generator.phone_number(),
            "E-post påmelder": self.generator.email(),
        }


def calculate_age_class(format: str, sex: SexLiteral, age: int) -> str:  # noqa: C901
    """Calculates age-class based on sex and age.

    Args:
        format (str): the format of the resulting contestant
        sex (SexLiteral): the sex of the contestant ('K' or 'M')
        age (int): the age of the contestant

    Returns:
        str: the age-class of the contestant
    """
    # TODO: This is not correct, but it is the best we can do for now.
    if format == "sportsadmin":
        if age < 17:
            if sex == "K":
                return f"J {age} år"
            else:
                return f"G {age} år"
        elif age < 19:
            if sex == "K":
                return f"K {age} år"
            else:
                return f"M {age} år"
        elif age < 21:
            if sex == "K":
                return "K 19/20 år"
            else:
                return "M 19/20 år"
        else:
            if sex == "K":
                return "Kvinner senior"
            else:
                return "Menn senior"
    else:
        if age < 17:
            if sex == "K":
                return f"Jenter {age}"
            else:
                return f"Gutter {age}"
        elif age < 19:
            if sex == "K":
                return f"Kvinner {age}"
            else:
                return f"Menn {age}"
        elif age < 21:
            if sex == "K":
                return "Kvinner 19-20"
            else:
                return "Menn 19-20"
        else:
            if sex == "K":
                return "Kvinner senior"
            else:
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
