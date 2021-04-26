from gutendex import Gutendex
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    Gutendex.get_gutendex_books(1)
