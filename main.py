import sqlite3
from library_db.books.book import Book;


class Library:
    """The Library system"""
    def __init__(self):
        """Creates a new library instance

        library_con         opens or creates the library database library.db
        library_cur         creates cursor that allows the execution of SQL commands
        """
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
    
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
                    description = input("Enter a short description (at least 2 characters): ")
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
    
    def add_new_book(self, title, genre, author, pages, cover, published_date, description, isbn, amount):
        return Book().add_new_book(title, genre, author, pages, cover, published_date, description, isbn, amount)

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



    

    