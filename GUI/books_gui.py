import tkinter as tk
from tkinter import messagebox
from main import Library




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