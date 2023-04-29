from book import Book
import json

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
        """Create a new library instance

        members       a list of objects containing the members of the library
        books         a list of objects containing the available books of the library
        """
        self.members = []
        self.books = []

    def import_books(self):
        """ Imports preexisting books from json file"""
        with open('book_data.json') as my_file:
            data = json.load(my_file)
        for book in data:
            new_book = Book(book['Title'], book['Author'], book['Pages'], book['Cover'], book['PublishedDate'], book['Description'], book['ISBN'], int(book['Amount']), book['ID'])
            for genre in book['Genres'].split(","):
                new_book.add_new_genre(genre)
            self.books.append(new_book)
    

    def find_book_with_isbn(self, isbn):
        """ Finds a book using its ISBN with list comprehension"""
        book_list =  [book for book in self.books if book.isbn == isbn]
        if book_list:
            return book_list[0]
        return None

    def calculate_book_id(self):
        """ Calculates a unique id for each book based on the previous book's id"""
        if not self.books:
            last_book_id = 'B0'
        else:
            last_book_id = self.books[-1].id
        next_id = 'B' + str(int(last_book_id[1:]) + 1)
        return next_id

    def add_new_book(self, title, genres, author, pages, cover, published_date, description, isbn, amount):
        """ Adds a new book to the library's database
            If the book already exists it appends any new
            genres the user enters to its genres list
            Also it adds the amount of copies the user
            enters to the existing book's amount"""
        listObj = []
        with open('book_data.json') as my_file:
            listObj = json.load(my_file)
        
        book_exists = self.find_book_with_isbn(isbn)

        if not book_exists:
            id = self.calculate_book_id()
            new_book = Book(title, author, pages, cover, published_date, description, isbn, amount, id)
            for genre in genres:
                new_book.add_new_genre(genre)
            
            string_genres = ",".join(new_book.genres)

            listObj.append({
                "Title" : f"{new_book.title}",
                "Genres" : f"{string_genres}",
                "Author" : f"{new_book.author}",
                "Pages" : f"{new_book.pages}",
                "Cover" : f"{new_book.cover}",
                "PublishedDate" : f"{new_book.published_date}",
                "Description" : f"{new_book.description}",
                "ISBN" : f"{new_book.isbn}",
                "Amount" : f"{new_book.amount}",
                "ID" : f"{new_book.id}"
            })
            
            self.books.append(new_book)
        else:
            for genre in genres:
                if genre not in book_exists.genres:
                    book_exists.add_new_genre(genre)
                    print(f'New genre added to {book_exists.title}.')
            
            book_exists.increase_copies(amount)
            for book in listObj:
                if book["ISBN"] == isbn:
                    book["Genres"] = ",".join(book_exists.genres)
                    book["Amount"] = book_exists.amount

            print('This book already exists in the database.')

        with open('book_data.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4, separators=(',', ': '))

    def sort_by_genre(self, genre):
        """ Returns a list of books in a specific genre"""
        return [book for book in self.books if genre in book.genres]

    def main(self):
        self.import_books()

my_library = Library()
my_library.main()



    