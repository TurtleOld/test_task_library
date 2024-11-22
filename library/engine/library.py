import json
from typing import List, Dict, Any


class Library:
    def __init__(self, filename: str = "library.json") -> None:
        """
        Инициализирует библиотеку с указанным именем файла для хранения книг.

        Аргументы:
            filename (str): Имя файла для загрузки/сохранения данных библиотеки.
            По умолчанию "library.json".
        """
        self.filename = filename
        self.books: List[Dict[str, Any]] = []
        self.load_books()

    def load_books(self) -> None:
        """
        Загружает книги из указанного JSON-файла в библиотеку.

        Если файл не найден или содержит недопустимый JSON,
        библиотека начинается с пустого списка книг.
        """
        try:
            with open(self.filename, "r") as file:
                self.books = json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Начинаем с пустой библиотеки.")
        except json.JSONDecodeError:
            print(
                f"Ошибка декодирования JSON из файла {self.filename}. Начинаем с пустой библиотеки."
            )
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    def save_books(self) -> None:
        """Сохраняет текущий список книг в указанный JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Аргументы:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        if any(book['title'] == title for book in self.books):
            print(f'Книга с названием {title} уже есть в библиотеке')
            return
        book_id = len(self.books) + 1
        book = {
            "id": book_id,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии",
        }
        self.books.append(book)
        self.save_books()
        print(f"Книга {title} сохранена с id {book_id}")

    def remove_book(self, book_id: int) -> None:
        """
        Удаляет книгу из библиотеки по ее ID.

        Аргументы:
            book_id (int): ID книги, которую нужно удалить.
        """
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с id {book_id} удалена")
                return
            print(f"Книга с id {book_id} не найдена")

    def search_books(self, query: str) -> List[Dict[str, Any]]:
        """
        Ищет книги по названию, автору или году издания.

        Аргументы:
            query (str): Запрос для поиска в названиях книг, именах авторов или годах.

        Возвращает:
            List[Dict[str, Any]]: Список книг, соответствующих критериям поиска.
        """
        results = [
            book
            for book in self.books
            if query.lower() in book["title"].lower()
            or query.lower() in book["author"].lower()
            or query == str(book["year"])
        ]
        return results

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.
        Если библиотека пуста, выводит соответствующее сообщение.
        """
        if not self.books:
            print("Библиотека пуста.")
            return

        for book in self.books:
            print(
                f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                f"Год: {book['year']}, Статус: {book['status']}"
            )

    def change_status(self, book_id: int, new_status: str) -> None:
        """
        Изменяет статус книги по ее ID.

        Аргументы:
            book_id (int): ID книги, статус которой нужно изменить.
            new_status (str): Новый статус книги. Должен быть либо "в наличии", либо "выдана".
        """
        if new_status not in ["в наличии", "выдана"]:
            print('Неверный статус. Доступные статусы: "в наличии", "выдана".')
            return

        for book in self.books:
            if book["id"] == book_id:
                book["status"] = new_status
                self.save_books()
                print(f'Статус книги с ID {book_id} изменен на "{new_status}".')
                return
        print(f"Книга с ID {book_id} не найдена.")
