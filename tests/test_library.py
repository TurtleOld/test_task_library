import os.path
import unittest

from library.engine.library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self) -> None:
        self.filename = "library.json"
        self.library = Library(filename=self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_book(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]["title"], "Новая книга")
        self.assertEqual(self.library.books[0]["author"], "Иван Иванов")
        self.assertEqual(self.library.books[0]["year"], 2024)
        self.assertEqual(self.library.books[0]["status"], "в наличии")

    def test_remove_book(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.library.remove_book(book_id=1)
        self.assertEqual(len(self.library.books), 0)

    def test_display_book(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.assertEqual(self.library.books[0], {
            "author": "Иван Иванов",
            "id": 1,
            "status": "в наличии",
            "title": "Новая книга",
            "year": 2024,
        })

    def test_search_book(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.assertTrue(self.library.search_books("Новая книга"))

    def test_change_status(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0]["status"], "выдана")

    def test_change_status_invalid(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.library.change_status(1, "неизвестный статус")
        self.assertEqual(self.library.books[0]["status"], "в наличии")

    def test_remove_nonexistent_book(self) -> None:
        self.library.add_book(title="Новая книга", author="Иван Иванов", year=2024)
        self.library.remove_book(999)
        self.assertEqual(len(self.library.books), 1)
