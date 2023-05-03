import requests
import random
from main import Library

class GoogleBooksApi:
    def __init__(self):
        self.new_library = Library()
        self.genres = ['Fantasy', 'Romance', 'Science Fiction', 'Dystopian', 'Education', 'Mystery', 'Spirituality', 'Horror']
    
    def get_response(self, genre, index):
        return requests.get(f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre.lower()}&printType=books&maxResults=20&startIndex={index}&key=AIzaSyA-3x0Tc_QuzHRnpvbfznkuzWrR-f1cRrM")
    
    def convert_isbn10_to_isbn13(self, isbn10):
        temp = '978' + isbn10[:-1]
        temp_list = [int(char) for char in list(temp)]
        total = 0
        for i in range(len(temp_list)):
            if i == 0 or i % 2 == 0:
                total += temp_list[i] * 1
            else:
                total += temp_list[i] * 3
        if total % 10 == 0:
            final_digit = 0
        else:
            final_digit = 10 - total % 10
        return temp + str(final_digit)

    def get_isbn13(self, item):
        isbn = ''
        for id in item['volumeInfo']['industryIdentifiers']:
            if id['type'] == 'ISBN_13':
                return id['identifier']
            if id['type'] == 'ISBN_10':
                return self.convert_isbn10_to_isbn13(id['identifier'])
        return isbn
    
    def get_random_amount(self):
        return random.randint(5, 50)
    
    def fetch_books(self, genre):
        for i in range(1, 400, 20):
            response = self.get_response(genre, i)
            try:
                for item in response.json()['items']:
                    isbn = self.get_isbn13(item)
                    amount = self.get_random_amount()
                    try:
                        self.new_library.add_new_book(item['volumeInfo']['title'], genre, ','.join(item['volumeInfo']['authors']), item['volumeInfo']['pageCount'], item['volumeInfo']['imageLinks']['thumbnail'], item['volumeInfo']['publishedDate'], item['volumeInfo']['description'], isbn, amount)
                    except KeyError as e:
                        book_name = item['volumeInfo']['title']
                        print(f'Key {e} not found for book: {book_name}')
            except KeyError as e:
                print(e) 
    
    def main_loop(self):
        for genre in self.genres:
            print(f"Fetching {genre} books")
            self.fetch_books(genre)                



books_api = GoogleBooksApi()
books_api.main_loop()
