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
        return [bookid for bookid in self.library_cur.execute("SELECT bookid FROM borrowed_books WHERE memberid = ? AND date_borrowed LIKE ?", (self.member_id, "___" + date,)).fetchall()]
    
    def get_preferences(self):
        pass


if __name__ == "__main__":
    print(MemberPreferences(10).get_dates())
    print(MemberPreferences(10).get_books_per_month("02/2023"))
    

            

    
