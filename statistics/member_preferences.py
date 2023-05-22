import sqlite3

class MemberPreferences:
    def __init__(self, member_id):
        self.member_id = member_id
        self.library_con = sqlite3.connect("library.db")
        self.library_cur = self.library_con.cursor()
        self.preferences = self.generate_preferences()
    
    def get_dates(self):
        return [date[0][3:] for date in self.library_cur.execute("SELECT date_borrowed FROM borrowed_books WHERE memberid = ?", (self.member_id,)).fetchall()]
    
    def get_books_per_month(self, date):
        return [bookid[0] for bookid in self.library_cur.execute("SELECT bookid FROM borrowed_books WHERE memberid = ? AND date_borrowed LIKE ?", (self.member_id, "___" + date,)).fetchall()]
    
    def find_book_genre(self, book_id):
        return [genre[0] for genre in self.library_cur.execute("SELECT genre FROM books WHERE bookid = ?", (book_id,)).fetchall()][0]

    def generate_preferences(self):
        prefs = {}
        for date in self.get_dates():
            monthly_prefs = {}
            for book in self.get_books_per_month(date):
                genre = self.find_book_genre(book)
                if genre in monthly_prefs.keys():
                    monthly_prefs[genre] += 1
                else:
                    monthly_prefs[genre] = 1
            prefs[date] = monthly_prefs
        return prefs
    
    def get_preferences(self):
        return self.preferences
            




if __name__ == "__main__":

    print(MemberPreferences(10).get_preferences())
    

            

    
