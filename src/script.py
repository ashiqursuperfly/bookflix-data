from gutendex import Gutendex
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    for i in range(5, 11):
        Gutendex.get_gutendex_books(i)
