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
    
    def __str__(self):
        print(f"Preference distribution of member {self.member_id} is:")
        for month, genres in self.preferences.items():
            print(month + ":")
            for genre, amount in genres.items():
                print(genre + ":" + str(amount))
            print()
        return ""
 
            




if __name__ == "__main__":

    print(MemberPreferences(11).get_preferences())
    print(MemberPreferences(11))
    

            

    
