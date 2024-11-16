from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey
from database.database import Base
import enum

__all__ = [
    "Book",
    "Language",
    "Genre",
    "Author",
    "Catalog",
    "Country",
    "Edition",
    "BookGenre",
    "BookAuthor",
    "BookCatalog",
    "Publisher",
    "Base",
]


class Language(Base):
    __tablename__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    editions: Mapped[list["Edition"]] = relationship(
        back_populates="language", uselist=True
    )


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="genres", uselist=True, secondary="book_genre"
    )


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="authors", uselist=True, secondary="book_author"
    )


class Catalog(Base):
    __tablename__ = "catalog"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(
        back_populates="catalogs", uselist=True, secondary="book_catalog"
    )


class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="country", uselist=True)


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    keywords: Mapped[str] = mapped_column(String(70), nullable=True)
    year_released: Mapped[int] = mapped_column(Integer, nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    # languages: Mapped[list["Language"]] = relationship(
    #     back_populates="books", uselist=True, secondary="book_language"
    # )
    catalogs: Mapped[list["Catalog"]] = relationship(
        back_populates="books", uselist=True, secondary="book_catalog"
    )
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books", uselist=True, secondary="book_author"
    )
    country: Mapped["Country"] = relationship(back_populates="books", uselist=False)
    editions: Mapped[list["Edition"]] = relationship(
        back_populates="book", uselist=True
    )
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="books", uselist=True, secondary="book_genre"
    )

    __table_args__ = (
        CheckConstraint(
            "year_realised > 0 AND year_realised <= 2024", name="book_year_released_chk"
        ),
    )


class BookCatalog(Base):
    __tablename__ = "book_catalog"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    catalog_id: Mapped[int] = mapped_column(ForeignKey("catalog.id"), nullable=False)


# class BookLanguage(Base):
#     __tablename__ = "book_language"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
#     language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)


class BookAuthor(Base):
    __tablename__ = "book_author"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)


class BookGenre(Base):
    __tablename__ = "book_genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), nullable=False)


class Status(enum.Enum):
    available = "Доступно"
    unavailable = "Недоступно"


class Publisher(Base):
    __tablename__ = "publisher"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    editions: Mapped[list["Edition"]] = relationship(
        back_populates="publisher", uselist=True
    )


class Edition(Base):
    __tablename__ = "edition"
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publisher.id"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    isbn_number: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    page_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    book: Mapped["Book"] = relationship(back_populates="editions", uselist=False)
    instances_available: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher: Mapped["Publisher"] = relationship(
        back_populates="editions", uselist=False
    )
    language: Mapped["Language"] = relationship(
        back_populates="editions", uselist=False
    )
    __table_args__ = (
        CheckConstraint(page_amount >= 0, name="edition_page_amount_chk"),
        CheckConstraint(
            (published_year > 0) & (published_year <= 2024),
            name="edition_published_year_chk",
        ),
        CheckConstraint("isbn_number LIKE '%-%-%-%-%'", name="edition_isbn_number_chk"),
        CheckConstraint(
            instances_available >= 1, name="edition_instances_available_chk"
        ),
    )
