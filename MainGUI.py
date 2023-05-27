import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Text
import sqlite3
from members.member_storage import MemberStorage
from members.manage_members import MemberManager
from main import Library
from borrowed_book import Borrow_Books
from members.validate_member_details import *


class LibraryGUI:
    def __init__(self, MainMenu):
        self.root = MainMenu
        self.root.title("Library Management System")
        self.root.geometry("800x300+200+200")

        self.title_label = tk.Label(MainMenu, text="Library Management System", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.members_button = tk.Button(MainMenu, text="Members", font=("Arial", 16, "bold"),
                                        command=self.open_members_view)
        self.members_button.pack(pady=10)

        self.books_button = tk.Button(MainMenu, text="Books", font=("Arial", 16, "bold"), command=self.open_books_view)
        self.books_button.pack(pady=10)

        self.statistics_button = tk.Button(MainMenu, text="Borrow Book", font=("Arial", 16, "bold"),
                                           command=self.open_borrow_book_view)
        self.statistics_button.pack(pady=10)

        # self.statistics_button = tk.Button(MainMenu, text="Statistics", command=self.open_statistics)
        # self.statistics_button.pack(pady=10)

        # self.exit_button = tk.Button(MainMenu, text="Close", command=MainMenu.quit)
        # self.exit_button.pack(pady=10)

    def open_members_view(self):
        members_window = tk.Toplevel(self.root)
        members_window.title("Members")
        members_gui = MemberManagerGUI(members_window)
        members_gui.master.mainloop()

    def open_books_view(self):
        books_window = tk.Toplevel(self.root)
        books_window.title("Books")
        books_gui = BooksGUI(books_window)
        books_gui.books.mainloop()

    def open_borrow_book_view(self):
        BorrowBooksGUI(self)

    def on_books_window_close(self, books_window):
        self.root.deiconify()
        books_window.destroy()


class MemberManagerGUI:
    def __init__(self, members):

        self.master = members
        self.member_manager = MemberManager()

        self.master.title("Member Manager")
        self.master.geometry("800x300+200+200")

        self.label = tk.Label(members, text="Member Manager options", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.add_member_button = tk.Button(members, text="Add new member", font=("Arial", 16, "bold"),
                                           command=self.add_new_member)
        self.add_member_button.pack(pady=10)

        self.update_member_button = tk.Button(members, text="Update member profile", font=("Arial", 16, "bold"),
                                              command=self.update_member_profile)
        self.update_member_button.pack(pady=10)

        self.renew_membership_button = tk.Button(members, text="Update member profile_backend",
                                                 font=("Arial", 16, "bold"), command=self.update_member_profile_backend)
        self.renew_membership_button.pack(pady=10)

        self.pause_membership_button = tk.Button(members, text="Pause/Renew membership", font=("Arial", 16, "bold"),
                                                 command=self.pause_renew_membership)
        self.pause_membership_button.pack(pady=10)

    def add_new_member(self):
        # Create a new window for adding a member
        add_new_member_window = tk.Toplevel(self.master)
        add_new_member_window.title("Add New Member")
        add_new_member_window.geometry("800x300+200+200")

        # Create labels and entry fields for member information
        name_label = tk.Label(add_new_member_window, text="Name:", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, sticky="w")
        name_entry = tk.Entry(add_new_member_window, width=30)
        name_entry.grid(row=0, column=1)

        address_label = tk.Label(add_new_member_window, text="Address:", font=("Arial", 16, "bold"))
        address_label.grid(row=1, column=0, sticky="w")
        address_entry = tk.Entry(add_new_member_window, width=30)
        address_entry.grid(row=1, column=1)

        phone_label = tk.Label(add_new_member_window, text="Phone Number:", font=("Arial", 16, "bold"))
        phone_label.grid(row=2, column=0, sticky="w")
        phone_entry = tk.Entry(add_new_member_window, width=30)
        phone_entry.grid(row=2, column=1)

        email_label = tk.Label(add_new_member_window, text="Email:", font=("Arial", 16, "bold"))
        email_label.grid(row=3, column=0, sticky="w")
        email_entry = tk.Entry(add_new_member_window, width=30)
        email_entry.grid(row=3, column=1)

        age_label = tk.Label(add_new_member_window, text="Age:", font=("Arial", 16, "bold"))
        age_label.grid(row=4, column=0, sticky="w")
        age_entry = tk.Entry(add_new_member_window, width=30)
        age_entry.grid(row=4, column=1)

        occupation_label = tk.Label(add_new_member_window, text="Occupation:", font=("Arial", 16, "bold"))
        occupation_label.grid(row=5, column=0, sticky="w")
        occupation_entry = tk.Entry(add_new_member_window, width=30)
        occupation_entry.grid(row=5, column=1)

        def save_member():
            # Get the entered information
            name = name_entry.get()
            if not validate_name(name):
                messagebox.showerror("Error",
                                     "Invalid name. Name must contain only valid characters: letters, spaces and dots in case of middle names")
                return

            address = address_entry.get()

            phone_number = phone_entry.get()
            if not validate_phone_number(phone_number):
                messagebox.showerror("Error",
                                     "Invalid Phone Number. Ensure that the phone number consists of digits, spaces, hyphens and optionally a country code (such as +30)")
                return

            email = email_entry.get()
            if not validate_email(email):
                messagebox.showerror("Error",
                                     "Invalid email address  Acceptable mail forms olny such as: \n'name@domain.tld'\n'name-surname@domain.tld'\n'name.surname@domain.tld'\n'name123@domain.tld'")
                return

            age = age_entry.get()
            if not validate_age(age):
                messagebox.showerror("Error", "Invalid age \nAge must be a integer number between 3 and 105")
                return

            occupation = occupation_entry.get()
            if not validate_occupation(occupation):
                messagebox.showerror("Error", "Occupation can`t be empty")
                return

            # Save the new member
            self.member_manager.add_new_member(name, address, phone_number, email, age, occupation)

            # Show a success message
            messagebox.showinfo("Success", "New member added successfully")

            # Close the window
            add_new_member_window.destroy()

        save_button = tk.Button(add_new_member_window, text="Save", font=("Arial", 16, "bold"), command=save_member)
        save_button.grid(row=6, column=1, sticky="w")

    def update_member_profile(self):
        add_new_member_window = tk.Toplevel(self.master)
        add_new_member_window.title("Update Member Profile")
        add_new_member_window.geometry("800x800+200+200")

        member_id_label = tk.Label(add_new_member_window, text="Memebr ID:", font=("Arial", 16, "bold"))
        member_id_label.grid(row=0, column=0, sticky="w")
        member_id_entry = tk.Entry(add_new_member_window, width=30)
        member_id_entry.grid(row=0, column=1)

        def search_member():
            # db connect
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # get member id
            member_id = member_id_entry.get()

            # get rows from database where member_id = member_id
            cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
            rows = cursor.fetchall()

            # check if the member exists
            if rows:
                #
                y_position = 100

                #
                fields = ['name', 'address', 'phone_number', 'email', 'age', 'occupation', 'status']
                text_boxes = []
                for row in rows:
                    for field, value in zip(fields, row[1:]):
                        label_field = Label(add_new_member_window, text=field)
                        label_field.place(x=50, y=y_position)
                        y_position += 30

                        text_box = Text(add_new_member_window, height=2, width=30)
                        text_box.place(x=150, y=y_position)
                        text_box.insert('end', str(value))
                        text_boxes.append(text_box)
                        y_position += 30

                #
                button_save = Button(add_new_member_window, text="Αποθήκευση",
                                     command=lambda: save_changes(rows, text_boxes))
                button_save.place(x=150, y=y_position + 30)

            # Add a message for no members found
            # else:

            # close db
            conn.close()

        def save_changes(rows, text_boxes):
            # db connect
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # update members fileds
            fields = ['name', 'address', 'phone_number', 'email', 'age', 'occupation', 'status']
            for row, text_box in zip(rows, text_boxes):
                member_id = row[0]
                values = [text_box.get("1.0", "end-1c"), row[2], row[7]] + list(row[3:7])

                cursor.execute(
                    "UPDATE members SET {} WHERE member_id = ?".format(','.join(f'{field}=?' for field in fields[0:])),
                    values + [member_id])

            # db commit and close
            conn.commit()
            conn.close()

        search_button = tk.Button(add_new_member_window, text="Search", font=("Arial", 16, "bold"),
                                  command=search_member)
        search_button.grid(row=2, column=1, sticky="w")

    def update_member_profile_backend(self):
        pass
        # member_id = self.get_member_id()
        # if member_id is not None:
        #     try:
        #         self.member_manager.manage_membership(renew=True)
        #         messagebox.showinfo("Success", "Membership successfully renewed!")
        #     except Exception as e:
        #         messagebox.showerror("Error", str(e))

    def pause_renew_membership(self):
        pass
        # member_id = self.get_member_id()
        # if member_id is not None:
        #     try:
        #         self.member_manager.manage_membership(renew=False)
        #         messagebox.showinfo("Success", "Membership paused successfully!")
        #     except Exception as e:
        #         messagebox.showerror("Error", str(e))

    def get_member_id(self):
        pass
        # member_id = simpledialog.askinteger("Member ID", "Please enter Member ID:")
        # return member_id


class BooksGUI:

    def __init__(self, books):
        self.books = books
        self.library = Library()
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI widgets"""
        self.books.title("Library System")

        # Title label
        title_label = tk.Label(self.books, text="Library Systems", font=("Arial", 24))
        title_label.pack(pady=20)

        # Add new book frame
        add_frame = tk.Frame(self.books)
        add_frame.pack()

        # Add new book labels and entry fields
        title_label = tk.Label(add_frame, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = tk.Entry(add_frame)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        genre_label = tk.Label(add_frame, text="Genre:")
        genre_label.grid(row=1, column=0, padx=10, pady=5)
        self.genre_entry = tk.Entry(add_frame)
        self.genre_entry.grid(row=1, column=1, padx=10, pady=5)

        author_label = tk.Label(add_frame, text="Author:")
        author_label.grid(row=2, column=0, padx=10, pady=5)
        self.author_entry = tk.Entry(add_frame)
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)

        pages_label = tk.Label(add_frame, text="Pages:")
        pages_label.grid(row=3, column=0, padx=10, pady=5)
        self.pages_entry = tk.Entry(add_frame)
        self.pages_entry.grid(row=3, column=1, padx=10, pady=5)

        cover_label = tk.Label(add_frame, text="Cover:")
        cover_label.grid(row=4, column=0, padx=10, pady=5)
        self.cover_entry = tk.Entry(add_frame)
        self.cover_entry.grid(row=4, column=1, padx=10, pady=5)

        published_date_label = tk.Label(add_frame, text="Published Date:")
        published_date_label.grid(row=5, column=0, padx=10, pady=5)
        self.published_date_entry = tk.Entry(add_frame)
        self.published_date_entry.grid(row=5, column=1, padx=10, pady=5)

        description_label = tk.Label(add_frame, text="Description:")
        description_label.grid(row=6, column=0, padx=10, pady=5)
        self.description_entry = tk.Entry(add_frame)
        self.description_entry.grid(row=6, column=1, padx=10, pady=5)

        isbn_label = tk.Label(add_frame, text="ISBN:")
        isbn_label.grid(row=9, column=0, padx=10, pady=5)
        self.isbn_entry = tk.Entry(add_frame)
        self.isbn_entry.grid(row=9, column=1, padx=10, pady=5)

        amount_label = tk.Label(add_frame, text="Amount:")
        amount_label.grid(row=10, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(add_frame)
        self.amount_entry.grid(row=10, column=1, padx=10, pady=5)

        # Add new book button
        add_button = tk.Button(self.books, text="Add New Book", command=self.add_new_book)
        add_button.pack(pady=10)

        # Sort books by genre frame
        sort_frame = tk.Frame(self.books)
        sort_frame.pack()

        # Sort books by genre label and entry field
        genre_sort_label = tk.Label(sort_frame, text="Sort by Genre:")
        genre_sort_label.grid(row=0, column=0, padx=10, pady=5)
        self.genre_sort_entry = tk.Entry(sort_frame)
        self.genre_sort_entry.grid(row=0, column=1, padx=10, pady=5)

        # Sort books by genre button
        sort_button = tk.Button(self.books, text="Sort", command=self.sort_by_genre)
        sort_button.pack(pady=10)

    def add_new_book(self):
        """Adds a new book using the input values from the GUI"""
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        author = self.author_entry.get()
        pages = self.pages_entry.get()
        cover = self.cover_entry.get()
        published_date = self.published_date_entry.get()
        description = self.description_entry.get()
        isbn = self.isbn_entry.get()
        amount = self.amount_entry.get()

        success = self.library.add_new_book(title, genre, author, pages, cover, published_date, description, isbn,
                                            amount)

        if success:
            messagebox.showinfo("Success", "Book added successfully")
            # Clear the entry fields
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)
            self.cover_entry.delete(0, tk.END)
            self.published_date_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.isbn_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add book")

    def sort_by_genre(self):
        """Sorts the books by genre using the input value from the GUI"""
        genre = self.genre_sort_entry.get()

        books = self.library.sort_by_genre(genre)

        if len(books) > 0:
            book_titles = [f"{book[1]} by {book[3]}" for book in books]
            messagebox.showinfo("Books by Genre", "\n".join(book_titles))
        else:
            messagebox.showinfo("Books by Genre", "No books found in this genre")


class BorrowBooksGUI:
    def __init__(self, root):

        self.root = root
        self.borrow_books = Borrow_Books()

        # Title label
        # title_label = tk.Label(self.root, text="Library System", font=("Arial", 24))
        # title_label.pack(pady=20)

        self.window = tk.Tk()
        self.window.title("Library Management System")

        self.search_frame = tk.Frame(self.window)
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search Book:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_book)
        self.search_button.pack(side=tk.LEFT)

        self.availability_frame = tk.Frame(self.window)
        self.availability_frame.pack(pady=10)

        self.availability_label = tk.Label(self.availability_frame, text="Check Availability \n(by ID):")
        self.availability_label.pack(side=tk.LEFT)

        self.availability_entry = tk.Entry(self.availability_frame, width=30)
        self.availability_entry.pack(side=tk.LEFT)

        self.availability_button = tk.Button(self.availability_frame, text="Check", command=self.check_availability)
        self.availability_button.pack(side=tk.LEFT)

        self.borrow_frame = tk.Frame(self.window)
        self.borrow_frame.pack(pady=10)

        self.borrow_book_id_label = tk.Label(self.borrow_frame, text="Book ID:")
        self.borrow_book_id_label.pack(side=tk.LEFT)

        self.borrow_book_id_entry = tk.Entry(self.borrow_frame, width=10)
        self.borrow_book_id_entry.pack(side=tk.LEFT)

        self.borrow_member_id_label = tk.Label(self.borrow_frame, text="Member ID:")
        self.borrow_member_id_label.pack(side=tk.LEFT)

        self.borrow_member_id_entry = tk.Entry(self.borrow_frame, width=10)
        self.borrow_member_id_entry.pack(side=tk.LEFT)

        self.borrow_button = tk.Button(self.borrow_frame, text="Borrow", command=self.borrow_book)
        self.borrow_button.pack(side=tk.LEFT)

        self.return_frame = tk.Frame(self.window)
        self.return_frame.pack(pady=10)

        self.return_book_id_label = tk.Label(self.return_frame, text="Book ID:")
        self.return_book_id_label.pack(side=tk.LEFT)

        self.return_book_id_entry = tk.Entry(self.return_frame, width=10)
        self.return_book_id_entry.pack(side=tk.LEFT)

        self.return_member_id_label = tk.Label(self.return_frame, text="Member ID:")
        self.return_member_id_label.pack(side=tk.LEFT)

        self.return_member_id_entry = tk.Entry(self.return_frame, width=10)
        self.return_member_id_entry.pack(side=tk.LEFT)

        self.return_button = tk.Button(self.return_frame, text="Return", command=self.return_book)
        self.return_button.pack(side=tk.LEFT)

    def search_book(self):
        search_item = self.search_entry.get()
        if search_item:
            results = self.borrow_books.search_book(search_item)
            if results == 0:
                messagebox.showinfo("Search Book", f"No results found for '{search_item}'.")
            else:
                messagebox.showinfo("Search Book", "Search results:\n\n" + self.format_search_results(results))
        else:
            messagebox.showerror("Error", "Please enter a search term.")

    def check_availability(self):
        book_id = self.availability_entry.get()
        if book_id:
            if self.borrow_books.search_bookid_if_exists(book_id):
                availability = self.borrow_books.book_availabilty_by_id(book_id)
                if availability == 0:
                    messagebox.showinfo("Check Availability", f"The book with ID {book_id} is not available.")
                else:
                    messagebox.showinfo("Check Availability",
                                        f"The book with ID {book_id} is available. Quantity: {availability}")
            else:
                messagebox.showerror("Error", f"The book ID {book_id} does not exist.")
        else:
            messagebox.showerror("Error", "Please enter a book ID.")

    def borrow_book(self):
        book_id = self.borrow_book_id_entry.get()
        member_id = self.borrow_member_id_entry.get()

        if book_id and member_id:
            if self.borrow_books.search_bookid_if_exists(book_id) and self.borrow_books.search_memberid_if_exists(
                    member_id):
                result = self.borrow_books.borrow_books(book_id, member_id)
                if result == 0:
                    messagebox.showinfo("Borrow Book", "The book is not available for borrowing.")
                else:
                    messagebox.showinfo("Borrow Book", "Borrowing of the book is complete.")
            else:
                messagebox.showerror("Error", "Invalid book ID or member ID.")
        else:
            messagebox.showerror("Error", "Please enter a book ID and member ID.")

    def return_book(self):
        book_id = self.return_book_id_entry.get()
        member_id = self.return_member_id_entry.get()

        if book_id and member_id:
            if self.borrow_books.search_bookid_if_exists(book_id) and self.borrow_books.search_memberid_if_exists(
                    member_id):
                self.borrow_books.return_books(book_id, member_id)
                messagebox.showinfo("Return Book", "The book was returned.")
            else:
                messagebox.showerror("Error", "Invalid book ID or member ID.")
        else:
            messagebox.showerror("Error", "Please enter a book ID and member ID.")

    def format_search_results(self, results):
        formatted_results = ""
        for book in results:
            formatted_results += f"ID: {book[0]}\nISBN: {book[8]}\nTitle: {book[1]}\nGenre: {book[2]}\nAuthor: {book[3]}\nPublished Date: {book[6]}\nAvailable: {'Yes' if book[9] else 'No'}\n\n"
        return formatted_results

    # def run(self):
    #     self.window.mainloop()


if __name__ == "__main__":
    MainMenu = tk.Tk()
    library_gui = LibraryGUI(MainMenu)
    MainMenu.mainloop()
