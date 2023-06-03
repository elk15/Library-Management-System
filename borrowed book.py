import sqlite3
from datetime import date

class Borrow_Books:
    def help(self):
        while True:
            print("1. SEARCH BOOK")
            print("2. AVAILABILITY BOOK AS ID")
            print("3. BORROW BOOK")
            print("4. RETURN BOOK")
            print("5. EXIT")
            choice = input()
            if choice == '1':
                item = input("Give a book's id/title/isbn/author/genre: ")
                if self.search_book(item) == 0:
                    print(f"Hmm, looks like we didn't find anything for {item}.")
                else:
                    print("Search results:")
                    x = self.search_book(item)
                    for book in x:
                        print(f"ID: {book[0]}\nISBN: {book[8]}\nTitle: {book[1]}\nGenre: {book[2]}\nAuthor: {book[3]}\nPublished Date: {book[6]}\nAvailable: {'Yes' if book[9] else 'No'}\n")
                print("-"*20)

            elif choice == '2':
                book_id = input("Give the book id to check if it exists: ")
                if not(self.search_bookid_if_exists(book_id)):
                    print("The book id does not exist.")
                else:
                    if self.book_availabilty_by_id(book_id) == 0:
                        print(f"The book with id:{book_id} is not available.")
                    else:
                        print("The amount of search book is ", self.book_availabilty_by_id(book_id))
                print("-"*20)

            elif choice == '3':
                book_id = input("Give the id for the book you want to borrow: ")
                while not(self.search_bookid_if_exists(book_id)):
                    book_id = input("Please give the correct id for the book you want to borrow: ")
                member_id = input("Give the id for the member, who want to borrow the book: ")
                while not(self.search_memberid_if_exists(member_id)):
                    member_id = input("Please give the correct id for the member, who want to borrow the book: ")
                if self.borrow_books(book_id, member_id) == 0:
                    print("The book is not available for borrow.")
                else:
                    print(f"Borrowing of the book is complete.")
                print("-" * 20)

            elif choice == '4':
                book_id = input("Give the id for a book you want to return: ")
                while not(self.search_bookid_if_exists(book_id)):
                    book_id = input("Please give the correct id for the book you want to borrow: ")
                member_id = input("Give the id for the member, who want to return a book: ")
                while not(self.search_memberid_if_exists(member_id)):
                    member_id = input("Please give the correct id for the member, who want to borrow the book: ")
                self.return_books(book_id, member_id )
                print("The book was returned.")

            elif choice == '5':
                break
            else:
                print("Please enter an integer from 1-5")

    # This function pass as an argument as a string and search this string into the database named 'library.db'
    # returns a list of books with the matching items or 0 if nothing found
    def search_book(self, search_book):
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM books WHERE isbn LIKE ? OR title LIKE ? OR author LIKE ? OR bookid LIKE ? OR genre LIKE ? ",
                    ('%' + search_book + '%', '%' + search_book + '%', '%' + search_book + '%', '%' + search_book + '%',
                     '%' + search_book + '%'))
                results = c.fetchall()
                if len(results) == 0:
                    return 0
                else:
                    return results
        except sqlite3.Error as err:
            print("Error: ", err)

    # This function pass as an argument as a string and search this string into the database if the member id exists and
    # returns 1 if exists and 0 if not
    def search_memberid_if_exists(self, search_member):
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM members WHERE member_id=?", (search_member,))
                results = c.fetchall()
                if len(results) == 0:
                    return 0
                else:
                    return 1
        except sqlite3.Error as err:
            print("Error: ", err)

    # This function pass as an argument as a string and search this string into the database if the book id exists and
    # returns 1 if exists and 0 if not
    def search_bookid_if_exists(self, search_member):
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM books WHERE bookid=?", (search_member,))
                results = c.fetchall()
                if len(results) == 0:
                    return 0
                else:
                    return 1
        except sqlite3.Error as err:
            print("Error: ", err)


    # This function pass an argument as a string, check the availability of a book and
    # returns if it is available 1 or not 0
    def book_availabilty_by_id(self, bookid):
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute("SELECT amount FROM books WHERE bookid=?", (bookid,))
                available = c.fetchone()[0]
                if available == 0:
                    return 0
                else:
                    return available
        except sqlite3.Error as err:
            print("Error: ", err)

    # This function pass as two arguments as  strings (book id and member id), check if the book is available for borrow
    # and return 0 if is not available or return 1, update the amount of book and insert a new registration into the
    # 'borrowed_books' table
    def borrow_books(self, bookid, memberid):
        today = str(date.today())
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute("SELECT amount FROM books WHERE bookid=?", (bookid,))
                available = c.fetchone()[0]
                if not available:
                    return 0
                else:
                    c.execute("UPDATE books SET amount=? WHERE bookid=?", ((available-1), bookid))
                    c.execute("INSERT OR IGNORE INTO borrowed_books(bookid, memberid, date_borrowed, is_returned) VALUES (?, ?, ?, ?)", (bookid, memberid, today, 0))
                    conn.commit()
                    return 1
        except sqlite3.Error as err:
            print("Error: ", err)

    # This function pass as two arguments as  ""trings (book id and member id) and return 1, update the amount
    # of book and update the 'is_returned' column of the 'borrowed_books' table.

    def return_books(self, bookid, memberid):
        try:
            with sqlite3.connect('library.db') as conn:
                c = conn.cursor()
                c.execute("SELECT amount FROM books WHERE bookid=?", (bookid,))
                available = c.fetchone()[0]
                c.execute("UPDATE books SET amount=? WHERE bookid=?", ((available + 1), bookid))
                c.execute("UPDATE borrowed_books SET is_returned=? WHERE bookid=? AND memberid=?", (1, bookid, memberid))
                conn.commit()
                return 1
        except sqlite3.Error as err:
            print("Error: ", err)


    def main(self):
        self.help()


if __name__ == "__main__":
    my_borrow_book = Borrow_Books()
    my_borrow_book.main()
