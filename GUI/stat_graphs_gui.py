
# ----------- Author: EvanSar --------- #

#Statistics Functions Import
from members.member_preferences import *
from statistics.compute_library_statistics import *

#Tkinter Imports
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont

#Matplotlib Imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Datetime object imports
from datetime import datetime

#Panda Module Imports
import pandas as pd

class LibraryStatisticsGUI:

    def __init__(self, db_filename: str, parent: tk.Tk):

        self.db_filename = db_filename
        self.parent = parent

        self.parent.title("Library Statistics")
        self.parent.geometry("600x600")
        self.parent.configure(bg="#FFFFFF")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=11, family="Inter")

        # Entry Fiels
        self.member_id_entry = tk.Entry(master=self.parent, width=25)
        self.member_id_entry_label = tk.Label(master=self.parent, text="Member ID: ") 
        self.member_id_entry_label.grid(row=0, column=0, padx=8, pady=10)
        self.member_id_entry.grid(row=0, column=1, padx=8, pady=10)

        self.start_date_entry = tk.Entry(master=self.parent, width=25)
        self.start_date_entry_label = tk.Label(master=self.parent, text="Start Date (MM/YYYY): ")
        self.start_date_entry_label.grid(row=1, column=0, padx=8, pady=10)
        self.start_date_entry.grid(row=1, column=1, padx=8, pady=10)

        self.end_date_entry = tk.Entry(master=self.parent, width=25)
        self.end_date_entry_label = tk.Label(master=self.parent, text="End Date (MM/YYYY): ")
        self.end_date_entry_label.grid(row=2, column=0, padx=8, pady=10)
        self.end_date_entry.grid(row=2, column=1, padx=8, pady=10)

        self.author_name_entry = tk.Entry(master=self.parent, width=25)
        self.author_name_entry_label = tk.Label(master=self.parent, text="Name of Author: ")
        self.author_name_entry_label.grid(row=3, column=0, padx=8, pady=10)
        self.author_name_entry.grid(row=3, column=1, padx=8, pady=10)

        # CTAs / Buttons
        self.count_books_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Borrowed Books for a Member", command=self.count_num_borrowed_books)
        self.count_books_button.grid(row=7, column=0, padx=8, pady=10)

        self.all_member_genre_preferences_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Genre Preferences in Timeframe", command=self.get_all_member_preferences_in_timeframe)
        self.all_member_genre_preferences_button.grid(row=7, column=1, padx=8, pady=10)

        self.borrowing_history_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Member Borrowing History", command=self.get_member_borrowing_history)
        self.borrowing_history_button.grid(row=8, column=0, padx=8, pady=10)

        self.stat_by_author_button= tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Books Borrowed by Author", command=self.get_stats_by_author)
        self.stat_by_author_button.grid(row=8, column=1, padx=8, pady=10)

        self.member_genre_preferences_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Single Member Genre Preference", command=self.get_member_preferences_in_timeframe)
        self.member_genre_preferences_button.grid(row=9, column=0, padx=8, pady=10)

        self.distribution_by_age_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Distribution by Age", command=self.distribution_borrowed_books_by_age)
        self.distribution_by_age_button.grid(row=9, column=1, padx=8, pady=10)        
        
        self.distribution_by_author_button = tk.Button(width=28, fg="#FFFFFF",bg="#0461ED",master=self.parent, text="Distribution by Author", command=self.distribution_borrowed_books_by_author)
        self.distribution_by_author_button.grid(row=10, column=0, padx=8, pady=10)

    def count_num_borrowed_books(self):
        member_id = self.member_id_entry.get()
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        if start_date_str.strip() == "" or end_date_str.strip() == "" or member_id.strip() == "":
            messagebox.showerror(title="Books borrowed by member", message="One or more of 'Date' and 'Member' Fields are empty") 

        if member_id.isdigit() and len(start_date_str) == 7 and len(end_date_str) == 7:
            start_date = datetime.strptime(start_date_str, "%m/%Y")
            end_date = datetime.strptime(end_date_str, "%m/%Y")
            library_stats = LibraryStatistics(self.db_filename)
            num_books = library_stats.count_num_books_in_timeframe(int(member_id), start_date, end_date)
            if num_books is not None:
                messagebox.showinfo(title="Number of Borrowed Books", message=f"The member with ID: {member_id} borrowed {num_books} books between {start_date_str} and {end_date_str}")
            else:
                messagebox.showerror(title="Error", message="Invalid input(s)")

    def get_all_member_preferences_in_timeframe(self):
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
       
        if start_date_str.strip() == "" or end_date_str.strip() == "":
            messagebox.showerror(title="Books borrowed by member", message="One or more of 'Date' Fields are empty") 

        else:
            if len(start_date_str) == 7 and len(end_date_str) == 7:
                start_date = datetime.strptime(start_date_str, "%m/%Y")
                end_date = datetime.strptime(end_date_str, "%m/%Y")
                library_stats = LibraryStatistics(self.db_filename)
                genre_distribution = library_stats.find_genre_preferences_in_timeframe(start_date, end_date)
                if genre_distribution is not None:
                    messagebox.showinfo(title="Genre Preferences", message=f"Genre distribution of member preferences for the period: {start_date_str} - {end_date_str}:\n{genre_distribution}")
                else:
                    messagebox.showerror(title="Error", message="Invalid input(s)")

    def get_member_preferences_in_timeframe(self):
        member_id = self.member_id_entry.get()

        if member_id.isdigit():
            library_stats = LibraryStatistics(self.db_filename)
            genre_distribution = library_stats.single_member_genre_preferences_in_timeframe(int(member_id))
            if genre_distribution is not None:
                messagebox.showinfo(title="Genre Preferences", message=f"Member with ID: {member_id} genre preferences: \n \n {genre_distribution}")
        else:
            messagebox.showerror(title="Error", message="Invalid input(s)")

    def get_member_borrowing_history(self):
        member_id = self.member_id_entry.get()

        if member_id.isdigit():
            library_stats = LibraryStatistics(self.db_filename)
            borrowed_books = library_stats.find_borrowed_books_for_member(int(member_id))
            if borrowed_books:
                messagebox.showinfo(title="Member Borrowing History", message=f"The member with id: {member_id} has borrowed the following books:\n{' -   '.join(borrowed_books)}")
            else:
                messagebox.showinfo(title="Member Borrowing History", message=f"The member with id: {member_id} has not borrowed any books yet")
        else:
            messagebox.showerror(title="Error", message="Invalid input(s)")

    def get_stats_by_author(self):
        author_name = self.author_name_entry.get()
        library_stats = LibraryStatistics(self.db_filename)
        stats_by_author = library_stats.stat_by_author(author_name)    
        
        if stats_by_author:
            messagebox.showinfo(title="Stats by Author",message=f"There are {stats_by_author} borrowed books for the author named: {author_name}")
        else:
            messagebox.showerror(title="Stats by Author", message="Invalid input(s)")

    def distribution_borrowed_books_by_age(self):
        window = tk.Tk()
        window.title("Borrowed Books Distribution by Age")
        window.geometry("500x500")

        fig = Figure(figsize=(5, 5), dpi=100)
        plot = fig.add_subplot(111)

        try:
            with sqlite3.connect(db_filename) as conn:
                query = '''
                        SELECT members.age, COUNT(*) as num_borrowed_books
                        FROM borrowed_books
                        JOIN members ON members.member_id = borrowed_books.memberid
                        GROUP BY members.age
                        '''
                df = pd.read_sql_query(query, conn)
                df.plot(kind='bar', x='age', y='num_borrowed_books', ax=plot)
                plot.set_xlabel('Age')
                plot.set_ylabel('Number of Borrowed Books')
                plot.set_title('Distribution of Borrowed Books by Age')

                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                tk.mainloop()
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def distribution_borrowed_books_by_author(self):

        window = tk.Tk()
        window.title("Borrowed Books Distribution by Author")
        window.geometry("1000x800")

        fig = Figure(figsize=(5, 5), dpi=100)
        plot = fig.add_subplot(111)

        try:
            with sqlite3.connect(db_filename) as conn:
                query = '''
                        SELECT books.author, COUNT(*) as num_borrowed_books
                        FROM borrowed_books
                        JOIN books ON books.bookid = borrowed_books.bookid
                        GROUP BY books.author
                        '''
                df = pd.read_sql_query(query, conn)
                df = df[:15]
                df.plot(kind='barh', x='author', y='num_borrowed_books', ax=plot)
                plot.set_xlabel('Number of Borrowed Books')
                plot.set_ylabel('Author')
                plot.set_title('Distribution of Borrowed Books by Author')

                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                tk.mainloop()
        except sqlite3.Error as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    db_filename = './library.db'
    root = tk.Tk()
    LibraryStatisticsGUI(db_filename, root)
    root.mainloop()







