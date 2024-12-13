from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, text
from database.database import Base

__all__ = [
    "Book",
    "Genre",
    "Author",
    "Catalog",
    "Country",
    "BookGenre",
    "BookAuthor",
    "BookCatalog",
    "Publisher",
    "Base",
]


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
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(800), nullable=False)
    page_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publisher.id", ondelete="RESTRICT"),
        nullable=False,
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id", ondelete="RESTRICT"), nullable=False
    )
    year_creation: Mapped[int] = mapped_column(Integer, nullable=False)
    year_published: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn_number: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    catalogs: Mapped[list["Catalog"]] = relationship(
        back_populates="books", uselist=True, secondary="book_catalog"
    )
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books", uselist=True, secondary="book_author"
    )
    country: Mapped["Country"] = relationship(back_populates="books", uselist=False)
    publisher: Mapped["Publisher"] = relationship(back_populates="books", uselist=False)
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="books", uselist=True, secondary="book_genre"
    )
    img_path: Mapped[str] = mapped_column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "year_creation > 0 AND year_creation <= 2024", name="book_year_creation_chk"
        ),
        CheckConstraint(
            "year_published > 0 AND year_published <= 2024",
            name="book_year_published_chk",
        ),
        CheckConstraint(page_amount >= 0, name="book_page_amount_chk"),
        CheckConstraint(quantity >= 1, name="book_quantity_chk"),
        CheckConstraint("isbn_number LIKE '%-%-%-%-%'", name="edition_isbn_number_chk"),
    )


class BookCatalog(Base):
    __tablename__ = "book_catalog"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    catalog_id: Mapped[int] = mapped_column(ForeignKey("catalog.id"), nullable=False)


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


class Publisher(Base):
    __tablename__ = "publisher"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(back_populates="publisher", uselist=True)


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60), nullable=False)

    # is_user: Mapped[bool] = mapped_column(
    #     nullable=False, server_default=text("true"), default=True
    # )
    # is_admin: Mapped[bool] = mapped_column(
    #     nullable=False, server_default=text("false"), default=False
    # )
    # is_staff: Mapped[bool] = mapped_column(
    #     nullable=False, server_default=text("false"), default=False
    # )


# class Edition(Base):
#     __tablename__ = "edition"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     publisher_id: Mapped[int] = mapped_column(
#         ForeignKey("publisher.id"), nullable=False
#     )
#     book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
#     isbn_number: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
#     page_amount: Mapped[int] = mapped_column(Integer, nullable=False)
#     status: Mapped[Status] = mapped_column(nullable=False)
#     published_year: Mapped[int] = mapped_column(Integer, nullable=False)
#     language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
#     book: Mapped["Book"] = relationship(back_populates="editions", uselist=False)
#     instances_available: Mapped[int] = mapped_column(Integer, nullable=False)
#     publisher: Mapped["Publisher"] = relationship(
#         back_populates="editions", uselist=False
#     )
#     language: Mapped["Language"] = relationship(
#         back_populates="editions", uselist=False
#     )
#     __table_args__ = (
#         CheckConstraint(page_amount >= 0, name="edition_page_amount_chk"),
#         CheckConstraint(
#             (published_year > 0) & (published_year <= 2024),
#             name="edition_published_year_chk",
#         ),
#         CheckConstraint("isbn_number LIKE '%-%-%-%-%'", name="edition_isbn_number_chk"),
#         CheckConstraint(
#             instances_available >= 1, name="edition_instances_available_chk"
#         ),
#     )


# class Language(Base):
#     __tablename__ = "language"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
#     editions: Mapped[list["Edition"]] = relationship(
#         back_populates="language", uselist=True
#     )
