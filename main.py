import sqlite3
import re
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
        self.existing_book_ids = [id[0] for id in self.library_cur.execute("SELECT bookid FROM books").fetchall()]
    
    def help(self):
        while True:
            print("Welcome! Select one of the following options:")
            print("1. Add new book")
            print("2. Sort books by genre")
            print("3. Exit")
            choice = input()
            if choice == '1':
                while True:
                    title = input("Enter the title (at least 2 characters): ")
                    genre = input("Enter the genre (at least 2 characters): ")
                    author = input("Enter the author (at least 2 characters): ")
                    pages = input("Enter the pages (positive integers only): ")
                    cover = input("Enter the link to the cover: ")
                    published_date = input("Enter the publication date (YYYY-MM-DD format months and days are optional): ")
                    author = input("Enter a short description (at least 2 characters): ")
                    isbn = input("Enter the ISBN-13 barcode of the book: ")
                    amount = input("Enter the amount of copies (positive integers only): ")
                    success = self.add_new_book(title, genre, author, pages, cover, published_date, description, isbn, amount)
                    if success:
                        break
            elif choice == '2':
                genre = input("Please choose a genre : Fantasy, Romance, Science Fiction, Dystopian, Education, Mystery, Spirituality, Horror: ")
                if len(self.sort_by_genre(genre)) == 0:
                    print("No such genre exists in the database or incorrect input")
                    continue
                for book in self.sort_by_genre(genre):
                    print(f"{book[1]} by {book[3]}")
            elif choice == '3':
                break
            else:
                print("Please enter an integer from 1-3")
    
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

    def sort_by_genre(self, genre):
        """Returns a list with books belonging in a specific category
        @author elina styliani papadimitriou
        """
        return [book for book in self.library_cur.execute("SELECT * FROM books WHERE genre = ?", (genre,)).fetchall()]

    def main(self):
       self.help()


if __name__ == "__main__":
    my_library = Library()
    my_library.main()



    

    