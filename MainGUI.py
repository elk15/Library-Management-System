import tkinter as tk

from member_manager_gui import MemberManagerGUI
from books_gui import BooksGUI
from borrow_books_gui import BorrowBooksGUI


class LibraryGUI:
    def __init__(self, MainMenu):
        self.MainMenu_window = MainMenu
        self.MainMenu_window.title("Library Management System")
        self.MainMenu_window.geometry("700x500+100+100")

        self.title_label = tk.Label(MainMenu, text="Library Management System", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20)

        button_width = 15  # πλάτος buttons

        self.members_button = tk.Button(MainMenu, text="Members", font=("Arial", 16, "bold"), width=button_width,
                                        command=self.open_members_view)
        self.members_button.pack(pady=10)

        self.books_button = tk.Button(MainMenu, text="Books", font=("Arial", 16, "bold"), width=button_width,
                                      command=self.open_books_view)
        self.books_button.pack(pady=10)

        self.borrow_button = tk.Button(MainMenu, text="Borrow Book", font=("Arial", 16, "bold"), width=button_width,
                                       command=self.open_borrow_book_view)
        self.borrow_button.pack(pady=10)

        self.statistics_button = tk.Button(MainMenu, text="Statistics", font=("Arial", 16, "bold"), width=button_width,
                                           command=self.open_statistics_view)
        self.statistics_button.pack(pady=10)

        self.exit_button = tk.Button(MainMenu, text="Close", font=("Arial", 16, "bold"), width=button_width,
                                     command=MainMenu.quit)
        self.exit_button.pack(pady=10)

    def open_members_view(self): # members window, κάνει minimize το MainMenu οταν πατηθεί και κάνει restore to MainMenu οταν κλείσει
        members_window = tk.Toplevel(self.MainMenu_window)
        members_window.title("Members")
        members_gui = MemberManagerGUI(members_window)
        self.MainMenu_window.iconify()

        def on_members_window_close():
            self.MainMenu_window.state('normal')
            members_window.destroy()

        members_window.protocol("WM_DELETE_WINDOW", on_members_window_close)
        members_gui.members_window.mainloop()

    def open_books_view(self): # books_view , κάνει minimize το MainMenu οταν πατηθεί και κάνει restore to MainMenu οταν κλείσει
        books_window = tk.Toplevel(self.MainMenu_window)
        books_window.title("Books")
        books_gui = BooksGUI(books_window)
        self.MainMenu_window.iconify()

        def on_open_books_view_close():
            self.MainMenu_window.state('normal')
            books_window.destroy()

        books_window.protocol("WM_DELETE_WINDOW", on_open_books_view_close)
        books_gui.books_window.mainloop()

    def open_borrow_book_view(self): # borrow_book , κάνει minimize το MainMenu οταν πατηθεί και κάνει restore to MainMenu οταν κλείσει
        borrow_books_window = tk.Toplevel(self.MainMenu_window)
        borrow_books_window.title("Borrow Books")
        borrow_books_gui = BorrowBooksGUI(borrow_books_window)
        self.MainMenu_window.iconify()

        def on_borrow_books_view_close():
            self.MainMenu_window.state('normal')
            borrow_books_window.destroy()

        borrow_books_window.protocol("WM_DELETE_WINDOW", on_borrow_books_view_close)
        borrow_books_gui.borrow_books_window.mainloop()

    def open_statistics_view(self):
        pass

    def on_books_window_close(self, books_window): # close button
        self.MainMenu_window.deiconify()
        books_window.destroy()


if __name__ == "__main__":
    MainMenu = tk.Tk()
    library_gui = LibraryGUI(MainMenu)
    MainMenu.mainloop()
