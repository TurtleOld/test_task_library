import os.path
from typing import Any, Generator

import pytest

from library.engine.library import Library


@pytest.fixture()
def library() -> Generator[Library, Any, None]:
    filename = "library.json"
    lib = Library(filename=filename)
    yield lib
    if os.path.exists(filename):
        os.remove(filename)


def test_add_book(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    assert len(library.books) == 1
    assert library.books[0]["title"] == "Новая книга"
    assert library.books[0]["author"] == "Иван Иванов"
    assert library.books[0]["year"] == 2024
    assert library.books[0]["status"] == "в наличии"


def test_remove_book(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    library.remove_book(book_id=1)
    assert len(library.books) == 0


def test_display_book(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    assert library.books[0] == {
        "author": "Иван Иванов",
        "id": 1,
        "status": "в наличии",
        "title": "Новая книга",
        "year": 2024,
    }


def test_search_book(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    assert library.search_books("Новая книга")


def test_change_status(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    library.change_status(1, "выдана")
    assert library.books[0]["status"] == "выдана"


def test_change_status_invalid(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    library.change_status(1, "неизвестный статус")
    assert library.books[0]["status"] == "в наличии"


def test_remove_nonexistent_book(library: Library) -> None:
    library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
    library.remove_book(999)
    assert len(library.books) == 1
