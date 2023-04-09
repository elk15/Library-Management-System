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
    def __init__(self, title, author, pages, cover, published_date, description, isbn, amount, id):
        self.title = title
        self.genres = []
        self.author = author
        self.pages = pages
        self.cover = cover
        self.published_date = published_date
        self.description = description
        self.isbn = isbn
        self.amount = amount
        self.id = id
    
    def add_new_genre(self, genre):
        self.genres.append(genre)

    def borrow_book(self):
        if self.amount > 0:
            self.amount -= 1
            return 1
        return 0
    
    def return_book(self):
        self.amount += 1
        return 1
    
    def __str__(self):
        return f'{self.title} by {self.author} publication date: {self.published_date}, pages: {self.pages},\n{self.genres}, description: {self.description} isbn: {self.isbn}, amount in inventory: {self.amount}, id: {self.id}'

class Library:
    def __init__(self):
        self.members = []
        self.books = []

    # Imports books from text file and adds them to the list(self.books)
    def import_books(self):
        with open('book_data.json') as my_file:
            data = json.load(my_file)
        for book in data:
            new_book = Book(book['Title'], book['Author'], book['Pages'], book['Cover'], book['PublishedDate'], book['Description'], book['ISBN'], int(book['Amount']), book['ID'])
            for genre in book['Genres'].split(","):
                new_book.add_new_genre(genre)
            self.books.append(new_book)
    

    def find_book_with_isbn(self, isbn):
        return [book for book in self.books if book.isbn == isbn][0]

    def calculate_book_id(self):
        if not self.books:
            last_book_id = 'B0'
        else:
            last_book_id = self.books[-1].id
        next_id = 'B' + str(int(last_book_id[1:]) + 1)
        return next_id

    # this function adds a new book if it doesn't already exist in the database
    # we use isbn-13
    # accepts a list of genres 
    def add_new_book(self, title, genres, author, pages, cover, published_date, description, isbn, amount):
        listObj = []
        with open('book_data.json') as my_file:
            listObj = json.load(my_file)

        if isbn not in [book.isbn for book in self.books]:
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
                if genre not in [book.genres for book in self.books if book.isbn == isbn][0]:
                    self.find_book_with_isbn(isbn).add_new_genre(genre)
                    for book in listObj:
                        if book["ISBN"] == isbn:
                            parts = book["Genres"].split(",")
                            parts.append(genre)
                            book["Genres"] = ",".join(parts)
            print('This book already exists in the database.')

        with open('book_data.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4, separators=(',', ': '))

    def sort_by_genre(self, genre):
        return [book for book in self.books if genre in book.genres]

    def main(self):
        self.import_books()


my_library = Library()
my_library.main()



    