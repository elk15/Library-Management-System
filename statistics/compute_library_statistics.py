import sqlite3
from typing import Optional, Tuple

from datetime import datetime
import pandas as pd

from members.member_storage import MemberStorage

DEFAULT_DB_PATH = './library.db'

def convert_str_to_datetime_obj(date: str) -> datetime:
    return datetime.strptime(date, "%d/%m/%Y")


class BorrowedBooksStorage:

    def __init__(self, db_filename: str):
        self._db_filename = db_filename

    def load_borrowed_books(self) -> pd.DataFrame:
        try:
            with sqlite3.connect(self._db_filename) as conn:
                return pd.read_sql_query("SELECT * FROM borrowed_books", conn)
        except sqlite3.Error as e:
            print(f"Error: {e}")


class BookStorage:

    def __init__(self, db_filename: str):
        self._db_filename = db_filename

    def load_books_by_ids(self, book_ids: Tuple[str]):
        try:
            with sqlite3.connect(self._db_filename) as conn:
                return pd.read_sql_query(f"SELECT * FROM books WHERE bookid in {book_ids}", conn)
        except sqlite3.Error as e:
            print(f"Error: {e}")
            
    def load_all_books(self):
        try:
            with sqlite3.connect(self._db_filename) as conn:
                return pd.read_sql_query(f"SELECT * FROM books", conn)
        except sqlite3.Error as e:
            print(f"Error: {e}")

class LibraryStatistics:

    def __init__(self, db_filename: str):
        borrowed_books_storage = BorrowedBooksStorage(db_filename)
        self.book_storage = BookStorage(db_filename)
        self.conn = sqlite3.connect(db_filename) #may be optional 
        self.member_storage = MemberStorage(db_filename).load_members()
        self.borrowed_books = borrowed_books_storage.load_borrowed_books()
        self.borrowed_books['date_borrowed'] = self.borrowed_books['date_borrowed'].apply(convert_str_to_datetime_obj)

    def count_num_books_in_timeframe(self, member_id: int, start_date: datetime, end_date: datetime) -> Optional[int]:
        borrowed_books = self.borrowed_books.where(
            (self.borrowed_books['memberid'] == member_id) &
            (self.borrowed_books['date_borrowed'] >= start_date) &
            (self.borrowed_books['date_borrowed'] <= end_date)
        )
        # number of books borrowed by the member with this id in the specified timeframe
        return borrowed_books['bookid'].count()

    def find_borrowed_books_for_member(self, member_id: int):
        borrowed_books_ids = self.borrowed_books.loc[self.borrowed_books['memberid'] == member_id, 'bookid']
        borrowed_books_ids = tuple(set(borrowed_books_ids.dropna()))

        if borrowed_books_ids:
            borrowed_books = self.book_storage.load_books_by_ids(borrowed_books_ids)
            return borrowed_books['title'].tolist()
        else:
            return list()

    def find_genre_preferences_in_timeframe(self, start_date: datetime, end_date: datetime) -> Optional[str]:
        borrowed_books_in_timeframe = self.borrowed_books.where(
            (self.borrowed_books['date_borrowed'] >= start_date) &
            (self.borrowed_books['date_borrowed'] <= end_date)
        )
        borrowed_books_ids = tuple(borrowed_books_in_timeframe['bookid'].dropna().unique())

        if not borrowed_books_ids:
            print(f'No statistics available for the specified period. Please try again with different start or/and '
                  f'end dates')
            return None

        borrowed_books = self.book_storage.load_books_by_ids(borrowed_books_ids)
        # gives the distribution of genre in borrowed books
        genre_distribution = borrowed_books['genre'].value_counts().to_string(header=False)
        return genre_distribution
    
    def single_member_genre_preferences_in_timeframe(self, member_id: int) -> Optional[str]:
        """Author: EvanSar"""
        
        borrowed_books_ids = self.borrowed_books.loc[self.borrowed_books['memberid'] == member_id, 'bookid']
        borrowed_books_ids = tuple(set(borrowed_books_ids.dropna()))

        if not borrowed_books_ids:
            print(f"No borrowed books available for member with id {member_id}")
            return None

        borrowed_books = self.book_storage.load_books_by_ids(borrowed_books_ids)
        # gives the distribution of genre in borrowed books
        genre_distribution = borrowed_books['genre'].value_counts().to_string(header=False)
        return genre_distribution
    
    def stat_by_author(self, author_name: str) -> int:
        """"Author: EvanSar"""
    
        try:
            query = f'''
            SELECT COUNT(*) AS num_borrowed_books
            FROM borrowed_books
            JOIN books ON books.bookid = borrowed_books.bookid
            WHERE books.author = "{author_name}"
            '''
            result = self.conn.execute(query).fetchone()
            return result[0]
        
        except sqlite3.Error as e:
                print(f"Error: {e}")


class LibraryStatisticsInput:

    LibraryStartDate = "04/2022"

    def __init__(self, db_filename: Optional[str] = None):

        db_filename = DEFAULT_DB_PATH if db_filename is None else db_filename
        self.library_stats = LibraryStatistics(db_filename)
        self.member_storage = MemberStorage(db_filename)

    def count_num_borrowed_books(self):

        member_id = self.get_member_id()
        if member_id is None:
            return None

        start_date, start_date_obj = self.get_date("Enter start date")
        if start_date_obj is None:
            return None

        end_date, end_date_obj = self.get_date("Enter end date")
        if end_date_obj is None:
            return None

        # check that start date is prior to end date
        if start_date_obj > end_date_obj:
            print("Invalid date range. The start date must be prior to the end date")
            return None

        num_books = self.library_stats.count_num_books_in_timeframe(member_id, start_date_obj, end_date_obj)
        if num_books is not None:
            print(f"The member with ID: {member_id} borrowed {num_books} books between {start_date} and {end_date}")

    def get_member_preferences_in_timeframe(self):

        start_date, start_date_obj = self.get_date("Enter start date")
        if start_date_obj is None:
            return None

        end_date, end_date_obj = self.get_date("Enter end date")
        if end_date_obj is None:
            return None

        # check that start date is prior to end date
        if start_date_obj > end_date_obj:
            print("Invalid date range. The start date must be prior to the end date")
            return None

        genre_distribution = self.library_stats.find_genre_preferences_in_timeframe(start_date_obj, end_date_obj)
        print(f"Genre distribution of member preferences for the period: {start_date} - {end_date}:"
              f"\n{genre_distribution}")

    def get_member_borrowing_history(self):
        member_id = self.get_member_id()

        if member_id is None:
            return None

        borrowed_books = self.library_stats.find_borrowed_books_for_member(member_id)
        if borrowed_books:
            print("The member with id: {} has borrowed the following books:\n{}".format(member_id,
                                                                                        '\n'.join(borrowed_books)))
        else:
            print(f"The member with id: {member_id} has not borrowed any books yet")

    def get_date(self, message) -> Tuple[str, Optional[datetime.date]]:

        while True:
            date = input(f"{message} (format: MM/YYYY) or press ENTER to exit: ")

            if not date:
                return date, None

            date_obj: datetime.date = self.validate_date(date)
            if date_obj:
                return date, date_obj

    def get_member_id(self) -> Optional[int]:
        """
        Prompt the user to enter a member ID and validate it.

        This function prompts the user to provide a member ID and performs validation to ensure its correctness.
        The entered member ID is used to identify a specific member in the system.
        """

        while True:
            member_id = input("Enter Member id (contains only digits) or press ENTER to exit: ")

            if not member_id:
                return None
            elif not member_id.isdigit():
                print("Invalid member id. Member ids are non negative integers")
            elif self.member_id_exists(int(member_id)):
                return int(member_id)

    @staticmethod
    def validate_date(date: str) -> Optional[datetime.date]:
        try:
            date_object = datetime.strptime(date, "%m/%Y")
        except ValueError:
            print(f"Invalid date format. Pleas provide a date in the following format: MM/YYYY")
            return None

        start_date = LibraryStatisticsInput.LibraryStartDate
        start_date_object = datetime.strptime(start_date, "%m/%Y")

        if (date_object < start_date_object) or (date_object > datetime.today()):
            print(f"Invalid date. Please select a date between: {start_date} and today")
            return None

        return date_object

    def member_id_exists(self, member_id) -> bool:
        member_prof = self.member_storage.load_member_by_id(member_id)
        return True if member_prof else False


if __name__ == "__main__":

    interface = LibraryStatisticsInput()

    while True:
        print("Library Statistics")
        print("========")
        print("1. Number of borrowed books in a given timeframe per member, ", end="")
        print("2. Book preferences per member, ", end="") 
        print("3. Genre preferences of all members in given a timeframe, ", end="")
        print("4. Member borrowing history, ", end="")
        print("5. Number of books borrowed per author ", end="") 
        print("6. Number of books borrowed per age ", end="") 
        print("7. Number of books borrowed per gender ") 

        choice = input("Enter your choice (or press enter to exit): ")

        if not choice:
            print("Exit")
            break
        elif choice == "1":
            interface.count_num_borrowed_books()
        elif choice == "2":
            pass
        elif choice == "3":
            interface.get_member_preferences_in_timeframe()
        elif choice == "4":
            interface.get_member_borrowing_history()
        elif choice == "5":
            pass
        elif choice == "6":
            pass
        elif choice == "7":
            pass
        else:
            print("Please enter a number between 1 and 7")
