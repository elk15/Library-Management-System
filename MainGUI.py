import tkinter as tk

from member_manager_gui import MemberManagerGUI
from books_gui import BooksGUI
from borrow_books_gui import BorrowBooksGUI

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


if __name__ == "__main__":
    MainMenu = tk.Tk()
    library_gui = LibraryGUI(MainMenu)
    MainMenu.mainloop()
