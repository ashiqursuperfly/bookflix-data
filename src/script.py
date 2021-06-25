from gutendex import Gutendex
from google_books import GoogleBooks
from dotenv import load_dotenv
from prisma_output import PrismaBook
import jsonpickle
from utils import write_file

LOCAL_FOLDER_JSON_DUMPS = "dumps"

if __name__ == "__main__":
    load_dotenv()
    for page in range(9, 11):
        books = Gutendex.get_gutendex_books(page)
        print(f"Page: {page} Book Count: {len(books)}")
        p_books = list()
        i = 0
        for book in books:
            print("Book:", i)
            p_book = Gutendex.parse_single_book(book)
            if p_book is not None:
                p_book: PrismaBook = p_book
                p_book = GoogleBooks.merge(p_book)
                p_books.append(p_book)
            i += 1
        write_file(f"{LOCAL_FOLDER_JSON_DUMPS}/{page}.json", jsonpickle.encode(p_books, unpicklable=False))

