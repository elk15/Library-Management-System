from typing import Optional, Tuple, Union, List
from itertools import chain

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

from statistics.compute_library_statistics import BorrowedBooksStorage, BookStorage

DEFAULT_DB_PATH = './library.db'


def preprocess_library_books(library_books: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the library books data by removing duplicate titles.

    Parameters:
    - library_books: A DataFrame containing information about library books.

    Returns:
     A new DataFrame with duplicated titles removed and the index reset.
    """
    if 'title' not in library_books.columns:
        raise KeyError("The 'title' column is not found in the DataFrame.")

    return library_books.drop_duplicates(subset=['title']).reset_index()


class BookRecommender:

    """

    Recommender system for suggesting books to library members based on their borrow history and library book data.

    Usage:
    >> recommender = BookRecommender()
    >> recommended_books = recommender.recommend_books(member_id, top_k)

    """

    def __init__(self,
                 library_db_path: Optional[str] = None,
                 sentence_encoding_model: Optional[str] = None):

        library_db_path = DEFAULT_DB_PATH if library_db_path is None else library_db_path

        if sentence_encoding_model is None:
            sentence_encoding_model = 'sentence-transformers/all-MiniLM-L6-v2'
            print(f"Defaulting to Sentence Transformer model: {sentence_encoding_model}")

        borrowed_book_storage = BorrowedBooksStorage(library_db_path)
        # loads all the records of borrowed books
        self.borrowed_books = borrowed_book_storage.load_borrowed_books()

        self.book_storage = BookStorage(library_db_path)
        # loads all the available books in the library
        library_books = self.book_storage.load_all_books()
        # simple preprocessing
        self.library_books = preprocess_library_books(library_books)

        self.model = SentenceTransformer(sentence_encoding_model)
        self.encoder = OneHotEncoder()
        self._fit_encoder()

    def recommend_books(self, member_id: str, top_k: Optional[int] = 3) -> Tuple:
        """
        Orchestrates the recommendation process by retrieving a list of top recommended books for a library member.

        The recommendation process involves the following steps:
        1. Loads the member's borrow history.
        2. Excludes the borrowed books from the recommendations.
        3. Creates vector representations for the member's history and the library books.
        4. Retrieves the indices of the top similar books to the member's history.
        5. Accesses these books by the indices and returns them as the recommended books.

        Parameters:
        - member_id: A unique identifier for the library member.
        - top_k: An integer specifying the number of top recommended books to retrieve.

        Returns:
        A tuple that contains the member borrowing history and a DataFrame with the top recommended books
        for the given member.
        """
        if (not isinstance(top_k, int)) or (top_k <= 0):
            raise ValueError("top_k must be a positive integer")

        # Loads member borrow history
        borrowed_books_ids = self.get_borrowed_books_ids_for_member(member_id)
        if not borrowed_books_ids:
            print(f"Member with ID {member_id} does not exist")
            return None, None

        member_history = self.book_storage.load_books_by_ids(borrowed_books_ids)

        # Excludes the borrowed books from the recommendations.
        library_books = self._filter_out_borrowed_books(member_history)

        # Creates vector representations
        member_profile_features = self._vectorise_borrowed_books(member_history)
        library_books_features = self._vectorise_library_books(library_books)

        # Retrieves the most similar books to the member history
        recommended_books_idx = self.retrieve_top_similar_book_indices(member_profile_features, library_books_features,
                                                                       top_k=top_k)
        recommended_books = library_books.loc[recommended_books_idx]

        return member_history, recommended_books

    def _fit_encoder(self):
        """
        Fits a OneHot encoder to the genre data of the library books.

        Returns:
        A fitted OneHotEncoder object that can be used for transforming the book genre into one-hot encoded format.
        """
        genre_data = self._convert_genre_column_to_array()
        self.encoder.fit(genre_data)

    def _filter_out_borrowed_books(self, member_history: pd.DataFrame) -> pd.DataFrame:
        """
        Removes books that have already been borrowed by the candidate from the available books
        for the recommendation system.

        Parameters:
        - member_history: A DataFrame representing the borrowing history of the candidate.

        Returns:
        A DataFrame containing available books that have not been borrowed by the candidate based
        on their borrowing history.
        """
        return self.library_books[~self.library_books.title.isin(member_history.title)].reset_index()

    def get_borrowed_books_ids_for_member(self, member_id: str) -> Tuple[str]:
        """
        Loads a tuple of book IDs for borrowed books from the library database based on a given member ID.

        Parameters:
        - member_id: The ID of the library member.

        Returns:
        A tuple of book IDs corresponding to the books borrowed by the member.
        """
        borrowed_books_ids = self.borrowed_books.loc[self.borrowed_books.memberid == int(member_id), 'bookid']
        return tuple(borrowed_books_ids)

    def _vectorise_borrowed_books(self, borrowed_books: pd.DataFrame) -> np.array:
        """
        Creates a vector representation of the books borrowed by a library member based on selected features
        such as book title, description, author, and genre.

        For the genre, which is a categorical feature, it creates one-hot embeddings.
        For the textual features (title, description, and author), it creates sentence embeddings.
        Then, it computes a single vector that represents the member's profile by averaging the embeddings for each book.

        Parameters:
        - borrowed_books: A DataFrame representing the borrowing history for the given member.

        Returns:
        A vector representation of the library member's borrowing history.
        """

        # vectorises genre
        genre_data = self._convert_genre_column_to_array(borrowed_books)
        genre_vectors = self._vectorise_book_genre(genre_data)

        # vectorises textual features
        embeddings = self.extract_embeddings_from_text_data(borrowed_books)

        # concatenates textual and categorical features
        borrowed_books_embeddings = self.concatenate_vectors(embeddings, genre_vectors)

        # creates an embedding that represents the user profile by averaging the embeddings of the borrowed books
        user_profile_embedding = borrowed_books_embeddings.mean(axis=0).reshape(1, -1)

        return user_profile_embedding

    def _vectorise_book_genre(self, genre_data: np.array):
        """
        Transforms the genre data into one-hot encoding representations.

        Parameters:
        - genre_data: A 2-d array containing the genre data to be transformed.

        Returns:
        An array object representing the one-hot encoding of the genre data
        """
        return self.encoder.transform(genre_data).toarray()

    def extract_embeddings_from_text_data(self, data: pd.DataFrame) -> Union[np.ndarray, List]:
        """
        Extracts embeddings from the textual data in the provided DataFrame.

        Parameters:
        - data: A pandas DataFrame containing the textual data to extract embeddings from.

        Returns:
        An array of embeddings representing the textual data.
        """
        text_columns = ['title', 'description', 'author']
        try:
            # concatenates textual features in a string
            text_features = data[text_columns].apply(' '.join, axis=1)
            return self.model.encode(text_features)
        except KeyError:
            raise KeyError(f"One of the text columns: {text_columns} was not found in the dataframe")

    @staticmethod
    def concatenate_vectors(embeddings: np.ndarray, genre_vectors: np.ndarray) -> np.ndarray:
        """
        Concatenates two 2D arrays, embeddings and genre_vectors, vertically along the y-axis.

        Parameters:
        - embeddings: A 2D array representing the embeddings.
        - genre_vectors: A 2D array representing the genre vectors.

        Returns:
        A new 2D array resulting from the vertical concatenation of embeddings and genre_vectors.
        """
        try:
            return np.concatenate((embeddings, genre_vectors), axis=1)
        except ValueError as e:
            raise Exception('The input arrays have incompatible shapes.') from e

    def _vectorise_library_books(self, library_books: pd.DataFrame) -> np.ndarray:
        """
        Creates vector representations for the books in the library by combining genre vectors and textual embeddings.

        Parameters:
         - library_books: A DataFrame containing the library books' information, including genre, author, description,
         and title.

        Returns:
        An array which constitutes a vector representation of the books' genre and textual features.
        """
        genre_data = self._convert_genre_column_to_array(library_books)
        genre_vectors = self._vectorise_book_genre(genre_data)
        book_embeddings = self.extract_embeddings_from_text_data(library_books)
        library_books_vectors = self.concatenate_vectors(book_embeddings, genre_vectors)
        return library_books_vectors

    @staticmethod
    def retrieve_top_similar_book_indices(user_profile: np.ndarray, library_books: np.ndarray, top_k):
        """
        Retrieves the indices of the top-k most similar books to the given user profile.

        Parameters:
        - user_profile: A vector representation of the user's preferences or history.
        - library_books: An array containing the vector representations of library books.
        - top_k: An integer specifying the number of top similar books to retrieve.

        Returns:
        A list of indices representing the top-k most similar books to the user profile.
        """
        # Computes the cosine similarity matrix between the user profile and library books
        similarity_matrix = cosine_similarity(user_profile, library_books)

        # Sorts the similarity matrix in ascending order
        sorted_similarity_indices = np.argsort(similarity_matrix, axis=1)
        sorted_indices_descending_order = np.flip(sorted_similarity_indices, axis=1)

        # Retrieves the indices of the top-k most similar books
        sorted_similarity_indices = sorted_indices_descending_order[:, :top_k]
        top_n_idx = list(chain(*sorted_similarity_indices))

        return top_n_idx

    def _convert_genre_column_to_array(self, books: pd.DataFrame = None) -> np.ndarray:
        """
        Converts the genre column in the given DataFrame into a 2D array format.

        Parameters:
        - books: A DataFrame containing the genre data.

        Returns:
        A 2D array containing the genre data.
        """

        if books is None:
            books = self.library_books

        if 'genre' not in books.columns:
            raise Exception('The library books dataset does not include a "genre" column.')

        return books.genre.to_numpy().reshape(-1, 1)


if __name__ == '__main__':

    recommender = BookRecommender()

    while True:
        member_id = input("Enter Member ID (contains only digits) or press ENTER to exit: ")

        if not member_id:
            print("Exiting...")
            break
        elif not member_id.isdigit():
            print("Invalid member ID. Member IDs must be non-negative integers.")
        else:
            user_profile, recommended_books = recommender.recommend_books(member_id, top_k=1)
            if recommended_books is not None:
                print(f"Borrowed books by member with ID {member_id}:")
                print(user_profile[['title', 'genre']].to_string(index=False))
                print("Recommended book:")
                print(recommended_books[['title', 'genre']].to_string(index=False))
                print("********************")











