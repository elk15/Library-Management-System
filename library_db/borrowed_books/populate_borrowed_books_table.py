import datetime
from typing import List
from itertools import chain
import random

import sqlite3
from datetime import date
from faker import Faker

from library_db.common import insert_data_into_table

NUM_MOCK_DATA = 100
DB_FILE_PATH = './library.db'


def create_mock_borrowed_books_data():
    faker = Faker()

    book_ids = load_column_from_table('books', 'bookid')
    member_ids = load_column_from_table('members', 'member_id')

    # random sampling from the population of books without replacement
    borrowed_book_ids = random.choices(book_ids, k=NUM_MOCK_DATA)

    # randomly assigns a member to each book
    table_data = []
    for book_id in borrowed_book_ids:
        random_member_id = random.choice(member_ids)
        random_date = faker.date_between(start_date='-1y', end_date='now')
        difference = datetime.date.today() - random_date
        is_returned = difference.days > 180
        random_date = date.strftime(random_date, "%d/%m/%Y")
        table_data.append((book_id, random_member_id, random_date, is_returned))

    return table_data


def load_column_from_table(table: str, column: str) -> List[str]:
    try:
        with sqlite3.connect(DB_FILE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {column} from {table}")
            book_ids = cursor.fetchall()
            return list(chain(*book_ids))
    except sqlite3.Error as e:
        print(f"Error while reading book ids: {e}")
        return list()


if __name__ == '__main__':

    borrowed_books = create_mock_borrowed_books_data()

    table_name = 'borrowed_books'
    table_columns = ('bookid', 'memberid', 'date_borrowed', 'is_returned')
    insert_data_into_table(DB_FILE_PATH, borrowed_books, table_name, table_columns)
