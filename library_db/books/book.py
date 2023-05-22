import sqlite3
import re
import uuid

class Book:
    "Book handling methods"
    def __init__(self):
        """Creates a new library instance

        library_con         opens or creates the library database library.db
        library_cur         creates cursor that allows the execution of SQL commands
        existing_book_ids   stores previously used book ids
        """
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
        self.existing_book_ids = [id[0] for id in self.library_cur.execute("SELECT bookid FROM books").fetchall()]

    def validate_book_input(self, title, genre, author, pages, cover, published_date, description, isbn, amount):
        """Checks if the input entered by the user when
        adding a new book is correct using regular expressions
        @author elina styliani papadimitriou
        """

        if len(str(title)) < 2 or len(str(genre)) < 2 or len(str(author)) < 2 or len(str(description)) < 2:
            print("Input must be at least 2 characters")
            return False
        try:
            if int(pages) <= 0 or int(amount) <= 0 or isinstance(pages, float) or isinstance(amount, float):
                print("Pages and amount must be a positive integer")
                return False
        except ValueError:
            print("Pages and amount must be a positive integer")
            return False
        if not re.fullmatch('^(?:[0-9]{4})(?:-(?:0[1-9]|1[0-2]))?(?:-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1]))?$', str(published_date)):
            print("Publication date must be in this format YYYY-MM-DD month and day are optional")
            return False
        if not re.fullmatch('^\S+\.\S+$', str(cover)):
            print("Cover must be a link")
            return False
        if not re.fullmatch('^[0-9]{13}$', str(isbn)):
            print("ISBN-13 must have a length of 13 integers")
            return False
        return True

    def check_if_book_exists(self, isbn):
        """Checks if a book already exists in the database using its isbn
        @author elina styliani papadimitriou
        """
        res = self.library_cur.execute("SELECT title FROM books WHERE isbn = ?", (isbn,))
        if res.fetchone() is None:
            return False
        return True

    def calculate_book_id(self):
        """Calculates a unique book id using uuid module
        @author elina styliani papadimitriou
        """
        bookid = "B" + str(uuid.uuid4())
        while bookid in self.existing_book_ids:
            bookid = "B" + str(uuid.uuid4())
        return bookid

    def add_new_book(self, title, genre, author, pages, cover, published_date, description, isbn, amount):
        """Adds a new book to the sqlite database 
        if the book already exists it only increases the amount
        @author elina styliani papadimitriou
        """
        if self.validate_book_input(title, genre, author, pages, cover, published_date, description, isbn, amount):
            if not self.check_if_book_exists(isbn):
                self.library_cur.execute("""
                INSERT INTO books VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (self.calculate_book_id(), title, genre, author, pages, cover, published_date, description, isbn, amount))
                self.library_con.commit()
                print(f"{title} succesfully added")
            else:
                self.library_cur.execute("""
                UPDATE books
                SET amount = amount + ?
                WHERE isbn = ?""", (amount, isbn))
                self.library_con.commit()
                print(f"{title} already exists in the database. Amount increased by {amount}")
            return True
        else:
            print("Failed to add new book")
            return False