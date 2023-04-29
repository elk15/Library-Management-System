from book import Book
import json
import sqlite3

class Member:
    """A library member"""
    def __init__(self, name, address, phone, email, age, occupation, id):
        """Create a new member instance
        
        The initial borrowed books list is empty

        name            the name of the member (eg. John Smith)
        address         the home address of the member (eg. Septembriou 7)
        phone           the member's phone number (eg. 6977024123)
        email           the member's email (eg. test@mail.com)
        age             the member's age (eg. 21)
        occupation      the member's job (eg. Doctor)
        id              the member's unique identification number (eg. M10)
        borrowed_books  a list containing the books a member has borrowed
        """
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.age = age
        self.occupation = occupation
        self.id = id
        self.borrowed_books=[]
    
    def borrow_book(self, book):
        """
        Adds a new book to the list of borrowed books
        returns False if the book already exists in the list
        returns True if it was added succesfully
        """
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            return True
        else:
            return False
    
    def return_book(self, book):
        """
        Removes a book from the list of borrowed books
        returns False if the book doesn't exist in the list
        returns True if it was removed succesfully
        """
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            return True
        else:
            return False



class Library:
    """The Library system"""
    def __init__(self):
        """Creates a new library instance

        library_con   opens or creates the library database library.db
        library_cur   creates cursor that allows the execution of SQL commands
        """
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
    

    def check_if_book_exists(self, isbn):
        """Checks if a book already exists in the database using its isbn"""
        res = cur.execute(f"SELECT title FROM books WHERE isbn = '{isbn}'")
        if res.fetchone() is None:
            return False
        return True

    def calculate_book_id(self):
        pass

    def add_new_book(self, title, genres, author, pages, cover, published_date, description, isbn, amount):
        pass


    def sort_by_genre(self, genre):
       pass

    def main(self):
       pass


if __name__ == "__main__":
    my_library = Library()



    