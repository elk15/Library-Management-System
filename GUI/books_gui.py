import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import re

from main import Library


class BooksGUI:

    def __init__(self, books):
        self.books_window = books
        self.library = Library()

        self.books_window.title("Books Management")
        self.books_window.geometry("700x500+100+100")

        title_label = tk.Label(self.books_window, text="Books Management", font=("Arial", 24))
        title_label.pack(pady=20)

        add_button = tk.Button(self.books_window, text="Add New Book", font=("Arial", 16, "bold"), command=self.open_add_book_window)
        add_button.pack(pady=20)

        sort_button = tk.Button(self.books_window, text="Sort by Genre", font=("Arial", 16, "bold"), command=self.open_sort_by_genre_window)
        sort_button.pack(pady=20)


    def open_add_book_window(self):
        #  add new book σε νεο παράθυρο
        add_new_book = tk.Toplevel()
        add_new_book.title("Add New Book")
        add_new_book.geometry("700x500+100+100")

        # Τα πεδία για το data entry των νέου βιβλίου
        title_label = tk.Label(add_new_book, text="Title:", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w")
        title_entry = tk.Entry(add_new_book, width=30)
        title_entry.grid(row=0, column=1)

        # το genre είναι επιλογή απο λίστα και οχι daya entry
        genre_label = tk.Label(add_new_book, text="Genre:", font=("Arial", 16, "bold"))
        genre_label.grid(row=1, column=0, sticky="w")
        genre_combobox = ttk.Combobox(add_new_book, values=["Fantasy", "Romance", "Science Fiction", "Dystopian", "Education", "Mystery", "Spirituality", "Horror", "Other"], width=27, state="readonly")
        genre_combobox.grid(row=1, column=1)

        author_label = tk.Label(add_new_book, text="Author:", font=("Arial", 16, "bold"))
        author_label.grid(row=2, column=0, sticky="w")
        author_entry = tk.Entry(add_new_book, width=30)
        author_entry.grid(row=2, column=1)

        pages_label = tk.Label(add_new_book, text="Pages:", font=("Arial", 16, "bold"))
        pages_label.grid(row=3, column=0, sticky="w")
        pages_entry = tk.Entry(add_new_book, width=30)
        pages_entry.grid(row=3, column=1)

        cover_label = tk.Label(add_new_book, text="Cover:", font=("Arial", 16, "bold"))
        cover_label.grid(row=4, column=0, sticky="w")
        cover_entry = tk.Entry(add_new_book, width=30)
        cover_entry.grid(row=4, column=1)

        published_date_label = tk.Label(add_new_book, text="Published Date:", font=("Arial", 16, "bold"))
        published_date_label.grid(row=5, column=0, sticky="w")
        published_date_entry = tk.Entry(add_new_book, width=30)
        published_date_entry.grid(row=5, column=1)

        description_label = tk.Label(add_new_book, text="Description:", font=("Arial", 16, "bold"))
        description_label.grid(row=6, column=0, sticky="w")
        description_entry = tk.Entry(add_new_book, width=30)
        description_entry.grid(row=6, column=1)

        isbn_label = tk.Label(add_new_book, text="ISBN:", font=("Arial", 16, "bold"))
        isbn_label.grid(row=7, column=0, sticky="w")
        isbn_entry = tk.Entry(add_new_book, width=30)
        isbn_entry.grid(row=7, column=1)

        amount_label = tk.Label(add_new_book, text="Amount:", font=("Arial", 16, "bold"))
        amount_label.grid(row=8, column=0, sticky="w")
        amount_entry = tk.Entry(add_new_book, width=30)
        amount_entry.grid(row=8, column=1)

        # Add new book button
        add_book_button = tk.Button(add_new_book, text="Add Book", font=("Arial", 16, "bold"),
                                    command=lambda: self.add_new_book(title_entry.get(), genre_combobox.get(),
                                                                      author_entry.get(), pages_entry.get(),
                                                                      cover_entry.get(), published_date_entry.get(),
                                                                      description_entry.get(), isbn_entry.get(),
                                                                      amount_entry.get(), add_new_book))
        add_book_button.grid(row=9, column=1, sticky="w")

    def add_new_book(self, title, genre, author, pages, cover, published_date, description, isbn, amount, window):
        """Adds a new book using the input values from the add book window"""
        # Έλεγχος για το πεδίο Pages
        if not pages.isdigit():
            messagebox.showerror("Error", "Please enter only numbers on Pages")
            return

        if not re.fullmatch('^\S+\.\S+$', str(cover)):
            messagebox.showerror("Error", "Please enter a valid cover format (example.com)")
            return

        # Έλεγχος για το πεδίο Published Date
        try:
            datetime.datetime.strptime(published_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format")
            return

        # Έλεγχος για το πεδίο ISBN
        if not isbn.isdigit() or len(isbn) != 13:
            messagebox.showerror("Error", "Please enter a 13-digit number for ISBN")
            return

        # Έλεγχος για το πεδίο Amount
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter only numbers for Amount")
            return

        success = self.library.add_new_book(title, genre, author, pages, cover, published_date, description, isbn, amount)

        if success:
            messagebox.showinfo("Success", "Book added successfully")
            window.destroy()
        else:
            messagebox.showerror("Error", "Failed to add book")

    def open_sort_by_genre_window(self):
        # sort books by genre σε νεο παράθυρο
        sort_window = tk.Toplevel()
        sort_window.title("Sort Books by Genre")
        sort_window.geometry("700x500+100+100")

        # Λιστα με τις επιλογές για το Genre
        genre_sort_label = tk.Label(sort_window, text="Genre:", font=("Arial", 16, "bold"))
        genre_sort_label.grid(row=0, column=0, padx=10, pady=5)
        genre_sort_entry = ttk.Combobox(sort_window, values=["Fantasy", "Romance", "Science Fiction", "Dystopian", "Education", "Mystery", "Spirituality", "Horror", "Other"], width=27, state="readonly")
        genre_sort_entry.grid(row=0, column=1, padx=10, pady=5)

        sort_books_button = tk.Button(sort_window, text="Sort Books", font=("Arial", 16, "bold"), command=lambda: self.sort_by_genre(genre_sort_entry.get(), sort_window))
        sort_books_button.grid(row=1, columnspan=2, pady=20)

    def sort_by_genre(self, genre, window):
        # εμφάνιση αποτελεσμάτων του search button (Sort Books)
        books = self.library.sort_by_genre(genre)

        if len(books) > 0:
            book_titles = [f"{book[1]} by {book[3]}" for book in books]
            messagebox.showinfo("Books by Genre", "\n".join(book_titles))
        else:
            messagebox.showinfo("Books by Genre", "No books found in this genre")

        window.destroy()
