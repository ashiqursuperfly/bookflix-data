import os
import requests
from prisma_output import PrismaBook
from utils import get_safe_value_from_dict


class GoogleBooks:
    BOOKS_ENDPOINT = f"https://www.googleapis.com/books/v1/volumes?q=<q>&projection=full&orderBy=relevance&key=<k>"
    BOOKS_ENDPOINT_AUTHOR = f"https://www.googleapis.com/books/v1/volumes?q=<q>+inauthor:<author>&projection=full&orderBy=relevance&key=<k>"

    class Params:
        items = "items"
        title = "title"
        type = "type"
        volumeInfo = "volumeInfo"
        averageRating = "averageRating"
        description = "description"
        bookshelves = "bookshelves"
        maturityRating = "maturityRating"
        identifier = "identifier"
        industryIdentifiers = "industryIdentifiers"
        published_date = "publishedDate"
        publisher = "publisher"

    class Const:
        ISBN_10 = "ISBN_10"
        ISBN_13 = "ISBN_13"

    @staticmethod
    def get_book_detail(name: str, author: str = ''):
        if author == '' or author is None:
            url = GoogleBooks.BOOKS_ENDPOINT.replace("<q>", name).replace("<k>", os.environ.get('GOOGLE_BOOKS_API_KEY'))
        else:
            url = GoogleBooks.BOOKS_ENDPOINT_AUTHOR.replace("<q>", name).replace("<author>", author).replace("<k>", os.environ.get('GOOGLE_BOOKS_API_KEY'))
        print('Google Books Url:', url)

        data = get_safe_value_from_dict(requests.get(url=url).json(), GoogleBooks.Params.items)

        if data is None or len(data) < 0:
            return None
        else:
            res = data[0][GoogleBooks.Params.volumeInfo]
            print('Google Books Entry Found:', res[GoogleBooks.Params.title], 'for book: ', name)
            return res

    @staticmethod
    def merge(p_book: PrismaBook):
        data = GoogleBooks.get_book_detail(p_book.title, p_book.get_first_author())

        if data is None:
            return p_book

        p_book.description = get_safe_value_from_dict(data, GoogleBooks.Params.description)
        p_book.rating = get_safe_value_from_dict(data, GoogleBooks.Params.averageRating)
        p_book.maturityRating = get_safe_value_from_dict(data, GoogleBooks.Params.maturityRating)
        p_book.yearPublished = get_safe_value_from_dict(data, GoogleBooks.Params.published_date)
        p_book.publisher = get_safe_value_from_dict(data, GoogleBooks.Params.publisher)

        isbns = get_safe_value_from_dict(data, GoogleBooks.Params.industryIdentifiers)
        if isbns is not None:
            for item in isbns:
                if get_safe_value_from_dict(item, GoogleBooks.Params.type) == GoogleBooks.Const.ISBN_10:
                    p_book.isbn10 = get_safe_value_from_dict(item, GoogleBooks.Params.identifier)
                if get_safe_value_from_dict(item, GoogleBooks.Params.type) == GoogleBooks.Const.ISBN_13:
                    p_book.isbn13 = get_safe_value_from_dict(item, GoogleBooks.Params.identifier)

        return p_book


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    print(GoogleBooks.get_book_detail('Alice', 'Lewis Carrol'))
