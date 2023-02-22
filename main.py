#Class that keeps track of each member and the books they have borrowed
class Member:
    #Create unique id for each member
    class_id = 0
    def __init__(self, name, address, phone, email, age, occupation):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.age = age
        self.occupation = occupation
        self.id = Member.class_id
        Member.class_id += 1
        self.borrowed_books=[]
    
    #Classes to allow members to borrow and return books
    #a member cant borrow a book he already has and
    #cant return a book he doesn't have. if transaction is succesful
    #returns 1 and an appropriate message if it fails it returns 0
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


    