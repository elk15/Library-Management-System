import requests
import random
from main import Library



new_library = Library()
new_library.main()

def fetch_books(genre):
    for i in range(1, 400, 20):
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre.lower()}&printType=books&maxResults=20&startIndex={i}&key=AIzaSyA-3x0Tc_QuzHRnpvbfznkuzWrR-f1cRrM")
        for item in response.json()['items']:
            isbn = ''
            for id in item['volumeInfo']['industryIdentifiers']:
                if id['type'] == 'ISBN_13':
                    isbn = id['identifier']
            if isbn == '':
                continue

            # insert random amount of books
            amount = random.randint(5, 50)

            genres = []
            genres.append(genre)
            try:
                for category in item['volumeInfo']['categories']:
                    genres.append(category)
            except KeyError:
                print('No categories')

            try:
                genres.append(item['volumeInfo']['mainCategory'])
            except KeyError:
                print('No main category')
                

            try:
                new_library.add_new_book(item['volumeInfo']['title'], genres, ','.join(item['volumeInfo']['authors']), item['volumeInfo']['pageCount'], item['volumeInfo']['imageLinks']['thumbnail'], item['volumeInfo']['publishedDate'], item['volumeInfo']['description'], isbn, amount)
            except KeyError as e:
                book_name = item['volumeInfo']['title']
                print(f'Key {e} not found for book: {book_name}')
                continue


# fetch_books('Fantasy')
# fetch_books('Romance')
# fetch_books('Science Fiction')
# fetch_books('Dystopia')
# fetch_books('Education')
# fetch_books('Mystery')
# fetch_books('Spirituality')
# fetch_books('Horror')