import tkinter as tk
from tkinter import messagebox

from borrowed_book import Borrow_Books


class BorrowBooksGUI:
    def __init__(self, borrow_books):

        self.borrow_books_window = borrow_books
        self.borrow_books = Borrow_Books()

        self.borrow_books_window.title("Library Management System")
        self.borrow_books_window.geometry("700x500+100+100")

        self.search_frame = tk.Frame(self.borrow_books_window)
        self.search_frame.pack(pady=10, fill=tk.X)
        self.search_label = tk.Label(self.search_frame, text="Search Book: \n(by: id/title/isbn/author\n or genre)", font=("Arial", 16, "bold"), anchor="w")
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_frame, text="Search", font=("Arial", 16, "bold"), command=self.search_book)
        self.search_button.pack(side=tk.LEFT)

        self.availability_frame = tk.Frame(self.borrow_books_window)
        self.availability_frame.pack(pady=10, fill=tk.X)
        self.availability_label = tk.Label(self.availability_frame, text="Check Availability \n(by ID):", font=("Arial", 16, "bold"), anchor="w")
        self.availability_label.pack(side=tk.LEFT)
        self.availability_entry = tk.Entry(self.availability_frame, width=30)
        self.availability_entry.pack(side=tk.LEFT)
        self.availability_button = tk.Button(self.availability_frame, text="Check", font=("Arial", 16, "bold"), command=self.check_availability)
        self.availability_button.pack(side=tk.LEFT)

        self.borrow_frame = tk.Frame(self.borrow_books_window)
        self.borrow_frame.pack(pady=10, fill=tk.X)
        self.borrow_book_id_label = tk.Label(self.borrow_frame, text="Book ID:", font=("Arial", 16, "bold"), anchor="w")
        self.borrow_book_id_label.pack(side=tk.LEFT)
        self.borrow_book_id_entry = tk.Entry(self.borrow_frame, width=30)
        self.borrow_book_id_entry.pack(side=tk.LEFT)
        self.borrow_member_id_label = tk.Label(self.borrow_frame, text="Member ID:", font=("Arial", 16, "bold"), anchor="w")
        self.borrow_member_id_label.pack(side=tk.LEFT)
        self.borrow_member_id_entry = tk.Entry(self.borrow_frame, width=10)
        self.borrow_member_id_entry.pack(side=tk.LEFT)
        self.borrow_button = tk.Button(self.borrow_frame, text="Borrow", font=("Arial", 16, "bold"), command=self.borrow_book)
        self.borrow_button.pack(side=tk.LEFT)

        self.return_frame = tk.Frame(self.borrow_books_window)
        self.return_frame.pack(pady=10, fill=tk.X)
        self.return_book_id_label = tk.Label(self.return_frame, text="Book ID:", font=("Arial", 16, "bold"), anchor="w")
        self.return_book_id_label.pack(side=tk.LEFT)
        self.return_book_id_entry = tk.Entry(self.return_frame, width=30)
        self.return_book_id_entry.pack(side=tk.LEFT)
        self.return_member_id_label = tk.Label(self.return_frame, text="Member ID:", font=("Arial", 16, "bold"), anchor="w")
        self.return_member_id_label.pack(side=tk.LEFT)
        self.return_member_id_entry = tk.Entry(self.return_frame, width=10)
        self.return_member_id_entry.pack(side=tk.LEFT)
        self.return_button = tk.Button(self.return_frame, text="Return", font=("Arial", 16, "bold"), command=self.return_book)
        self.return_button.pack(side=tk.LEFT)

    def search_book(self):
        search_item = self.search_entry.get()
        if search_item:
            results = self.borrow_books.search_book(search_item)
            if results == 0:
                messagebox.showinfo("Search Book", f"No results found for '{search_item}'.")
            else:
                self.display_results_window(results)
        else:
            messagebox.showerror("Error", "Please enter a search term.")

    def display_results_window(self, results):
        # Νεο παράθυρο με  τααποτελέσματε της αναζήτησης
        results_window = tk.Toplevel()
        results_window.title("Search Results")

        # Αποτελέσματα αναζήτησης σε text
        results_textbox = tk.Text(results_window, font=("Arial", 12))
        results_textbox.pack()


        for book in results:
            formatted_result = f"ID: {book[0]}\nISBN: {book[8]}\nTitle: {book[1]}\nGenre: {book[2]}\nAuthor: {book[3]}\nPublished Date: {book[6]}\nAvailable: {'Yes' if book[9] else 'No'}\n\n"
            results_textbox.insert(tk.END, formatted_result)

        # αμυντικός μηχανισμός για αν μην μπορεί ο user να πειράξει τα results στο text
        results_textbox.config(state=tk.DISABLED)
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
