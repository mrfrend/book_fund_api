from schemas.books import *
from sqlalchemy import select
from database.models import Country
from schemas.books import CountryDTO, CountryAddDTO
from database.database import session_factory


class CountryRepository:
    @classmethod
    def get_countries(cls) -> list[CountryDTO]:
        with session_factory() as session:
            query = select(Country)
            res = session.execute(query).scalars().all()
            countries_dto = [
                CountryDTO.model_validate(country, from_attributes=True)
                for country in res
            ]
            return countries_dto

    @classmethod
    def get_country(cls, country_id: int) -> CountryDTO | None:
        with session_factory() as session:
            country = session.get(Country, country_id)
            if country is None:
                return None
            return CountryDTO.model_validate(country, from_attributes=True)

    @classmethod
    def add_country(cls, data: CountryAddDTO) -> int:
        with session_factory() as session:
            country_dict = data.model_dump()
            country = Country(**country_dict)
            session.add(country)
            session.commit()
            session.refresh(country)
            return country.id

    @classmethod
    def delete_country(cls, country_id: int) -> 0 | 1:
        with session_factory() as session:
            query = select(Country).where(Country.id == country_id)
            country = session.execute(query).scalar_one_or_none()
            if country:
                session.delete(country)
                session.commit()
                return 1
            return 0
