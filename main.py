import json

# Class that keeps track of each member and the books they have borrowed
class Member:
    def __init__(self, name, address, phone, email, age, occupation, id):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.age = age
        self.occupation = occupation
        self.id = id
        self.borrowed_books=[]
    
    # Classes to allow members to borrow and return books
    # a member cant borrow a book he already has and
    # cant return a book he doesn't have. if transaction is succesful
    # returns 1 and an appropriate message if it fails it returns 0
    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            return 1
        else:
            return 0
    
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            return 1
        else:
            return 0

class Book:
    def __init__(self, title, genre, author, isbn, amount, id):
        self.title = title
        self.genre = genre
        self.author = author
        self.isbn = isbn
        self.amount = amount
        self.id = id
    
    def borrow_book(self):
        if self.amount > 0:
            self.amount -= 1
            return 1
        return 0
    
    def return_book(self):
        self.amount += 1
        return 1
    
    def __str__(self):
        return f'{self.title} by {self.author}, {self.genre}, isbn: {self.isbn}, amount in inventory: {self.amount}, id: {self.id}'

class Library:
    def __init__(self):
        self.members = []
        self.books = []

    # Imports books from text file and adds them to the list(self.books)
    def import_books(self):
        with open('book_data.json') as my_file:
            data = json.load(my_file)
        for book in data:
            new_book = Book(book['Title'], book['Genre'], book['Author'], book['ISBN'], int(book['Amount']), book['ID'])
            self.books.append(new_book)

    def calculate_book_id(self):
        last_book_id = self.books[-1].id
        next_id = 'B' + str(int(last_book_id[1:]) + 1)
        return next_id

    # this function adds a new book if it doesn't already exist in the database
    # we use isbn-13
    def add_new_book(self, title, genre, author, isbn, amount):
        if isbn not in [book.isbn for book in self.books]:
            id = self.calculate_book_id()
            new_book = Book(title, genre, author, isbn, amount, id)
            
            listObj = []
            with open('book_data.json') as my_file:
                listObj = json.load(my_file)
            listObj.append({
                "Title" : f"{new_book.title}",
                "Genre" : f"{new_book.genre}",
                "Author" : f"{new_book.author}",
                "ISBN" : f"{new_book.isbn}",
                "Amount" : f"{new_book.amount}",
                "ID" : f"{new_book.id}"
            })
            with open('book_data.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4, separators=(',', ': '))

            self.books.append(new_book)
        else:
            print('This book already exists in the database.')

    def sort_by_genre(self, genre):
        return [book for book in self.books if book.genre == genre]

    def main(self):
        self.import_books()
        for book in self.books:
            print(book)
        for book in self.sort_by_genre('Romance'):
            print(book)

my_library = Library()
my_library.main()


    