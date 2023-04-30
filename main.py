from book import Book
import sqlite3
import uuid

class Library:
    """The Library system"""
    def __init__(self):
        """Creates a new library instance

        library_con         opens or creates the library database library.db
        library_cur         creates cursor that allows the execution of SQL commands
        existing_book_ids   stores previously used book ids
        """
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
        self.existing_book_ids = set(self.library_cur.execute("SELECT bookid FROM books"))
    

    def check_if_book_exists(self, isbn):
        """Checks if a book already exists in the database using its isbn"""
        res = self.library_cur.execute("SELECT title FROM books WHERE isbn = ?", (str(isbn),))
        if res.fetchone() is None:
            return False
        return True

    def calculate_book_id(self):
        """Calculates a unique book id using uuid module"""
        bookid = "B" + str(uuid.uuid4())
        while bookid in self.existing_book_ids:
            bookid = "B" + str(uuid.uuid4())
        return bookid

    def add_new_book(self, title, genre, author, pages, cover, published_date, description, isbn, amount):
        """Adds a new book to the sqlite database 
        if the book already exists it only increases the amount"""
        if not self.check_if_book_exists(isbn):
            self.library_cur.execute("""
            INSERT INTO books VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.calculate_book_id(), title, genre, author, pages, cover, published_date, description, isbn, amount))
            self.library_con.commit()
        else:
            self.library_cur.execute("""
            UPDATE books
            SET amount = amount + ?
            WHERE isbn = ?""", (amount, isbn))
            self.library_con.commit()

    def sort_by_genre(self, genre):
        """Returns iterable with tuples"""
        return self.library_cur.execute("SELECT * FROM books WHERE genre = ?", (genre,))

    def main(self):
       pass


if __name__ == "__main__":
    my_library = Library()

    # check_if_book_exists tests
    # expects True
    print(my_library.check_if_book_exists('9781442457027'))
    print(my_library.check_if_book_exists(9781442457027))
    # expects False
    print(my_library.check_if_book_exists(9781))
    print(my_library.check_if_book_exists(False))
    print(my_library.check_if_book_exists(' '))
    print(my_library.check_if_book_exists('1081442457027'))
    print(my_library.check_if_book_exists('108144245702754'))

    

    