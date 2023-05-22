import sqlite3

class MemberPreferences:
    def __init__(self, member_id):
        self.member_id = member_id
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
        self.preferences = {}
    
    def get_dates(self):
        return [date[0][3:] for date in self.library_cur.execute("SELECT date_borrowed FROM borrowed_books WHERE memberid = ?", (self.member_id,)).fetchall()]
    
    def get_books_per_month(self, date):
        return [bookid[0] for bookid in self.library_cur.execute("SELECT bookid FROM borrowed_books WHERE memberid = ? AND date_borrowed LIKE ?", (self.member_id, "___" + date,)).fetchall()]
    
    def find_book_genre(self, book_id):
        return [genre[0] for genre in self.library_cur.execute("SELECT genre FROM books WHERE bookid = ?", (book_id,)).fetchall()][0]

    def get_preferences(self):
        pass


if __name__ == "__main__":
    print(MemberPreferences(10).get_dates())
    print(MemberPreferences(10).get_books_per_month("02/2023"))
    print(MemberPreferences(10).find_book_genre('Bf7902450-f802-4218-8150-7d9284842299'))
    

            

    
