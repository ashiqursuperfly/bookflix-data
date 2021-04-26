from utils import *
import requests
from prisma_output import *
import jsonpickle

LOCAL_FOLDER_BOOKS = "books"
LOCAL_FOLDER_COVERS = "covers"

S3_FOLDER_BOOKS = "books"
S3_FOLDER_COVERS = "book-covers"


class Gutendex:
    BOOKS_ENDPOINT = "https://gutendex.com/books?page=$"

    class Params:
        results = "results"
        title = "title"
        authors = "authors"
        copyright = "copyright"
        subjects = "subjects"
        formats = "formats"

        name = "name"
        birth_year = "birth_year"
        death_year = "death_year"

        class Formats:
            epub = "application/epub+zip"
            pdf = "application/pdf"
            image = "image/"

    @staticmethod
    def is_valid_book(book):
        if Gutendex.Params.title not in book:
            return False

        formats = get_safe_value_from_dict(book, Gutendex.Params.formats)
        if formats is None:
            return False

        pdf = str(get_safe_value_from_dict(formats, Gutendex.Params.Formats.pdf))
        epub = str(get_safe_value_from_dict(formats, Gutendex.Params.Formats.epub))

        if pdf is None and epub is None:
            return False
        elif epub.endswith("zip") and pdf is None:  # sometimes application/epub+zip provides zips. we ignore them
            return False
        return True

    @staticmethod
    def generate_pdf_cover_url(book):
        formats = dict(get_safe_value_from_dict(book, Gutendex.Params.formats))
        remote_cover = None

        for k in formats.keys():
            if str(k).startswith(Gutendex.Params.Formats.image):
                remote_cover = formats[k]
                break

        if remote_cover is None:
            return None

        filename = remote_cover.split("/")[-1]
        local_file = download(remote_cover, filename, LOCAL_FOLDER_COVERS)
        s3_key = f"{S3_FOLDER_COVERS}/{filename}"

        result = upload_s3(local_file, s3_key)

        if result:
            print("Generated cover img from pdf", s3_key)
        return None if not result else s3_key

    @staticmethod
    def generate_epub_cover_url(epub_filename, local_epub_path):
        pil = Image.open(get_epub_cover(local_epub_path))

        img_filename = f"{epub_filename}.{str(pil.format).lower()}"
        local_cover = f"{LOCAL_FOLDER_COVERS}/{img_filename}"
        pil.save(local_cover)

        s3_key = f"{S3_FOLDER_COVERS}/{img_filename}"
        result = upload_s3(local_cover, s3_key)

        return None if not result else s3_key

    @staticmethod
    def generate_book_file_and_cover(book):
        formats = get_safe_value_from_dict(book, Gutendex.Params.formats)
        pdf = get_safe_value_from_dict(formats, Gutendex.Params.Formats.pdf)
        epub = get_safe_value_from_dict(formats, Gutendex.Params.Formats.epub)
        s3_book_cover_key = None

        if epub is not None:
            file = epub
            file_type = "epub"
        else:
            file = pdf
            file_type = "pdf"

        filename = file.split("/")[-1]
        local_file = download(file, filename, LOCAL_FOLDER_BOOKS)
        s3_key = f"{S3_FOLDER_BOOKS}/{filename}"

        if file_type == "epub":
            s3_book_cover_key = Gutendex.generate_epub_cover_url(filename, local_file)

        if s3_book_cover_key is None or file_type == "pdf":
            s3_book_cover_key = Gutendex.generate_pdf_cover_url(book)

        result = upload_s3(local_file, s3_key)
        return None if not result else (file_type, s3_key, s3_book_cover_key)

    @staticmethod
    def parse_single_author(author):
        p_author = PrismaAuthorsConnectOrCreate()

        _ = get_safe_value_from_dict(author, Gutendex.Params.name)
        if _ is None:
            return None

        p_author.create = PrismaCreateAuthor()
        p_author.create.name = _
        p_author.create.birth_year = get_safe_value_from_dict(author, Gutendex.Params.birth_year)
        p_author.create.death_year = get_safe_value_from_dict(author, Gutendex.Params.death_year)

        p_author.where = PrismaWhere()
        p_author.where.name = _

        return p_author

    @staticmethod
    def parse_authors(book):
        _ = get_safe_value_from_dict(book, Gutendex.Params.authors)
        authors = _ if _ is not None else list()
        p_authors = PrismaAuthors()
        for author in authors:
            p_author = Gutendex.parse_single_author(author)
            if p_author is not None:
                p_authors.connect_or_create.append(p_author)

        return p_authors

    @staticmethod
    def parse_single_book(book):
        p_book = PrismaBook()

        if not Gutendex.is_valid_book(book):
            return None

        p_book.title = book[Gutendex.Params.title]

        file_type, book_url, book_cover_url = Gutendex.generate_book_file_and_cover(book)

        if book_url is None:
            print("Error: uploading to s3. Aborting Script.")
            quit()

        p_book.file_url = book_url
        p_book.file_type = file_type
        p_book.cover_image_url = book_cover_url

        _ = get_safe_value_from_dict(book, Gutendex.Params.copyright)
        p_book.copyright = _ if _ is not None else False

        p_book.authors = Gutendex.parse_authors(book)

        return p_book

    @staticmethod
    def get_gutendex_books(page: int):
        data = requests.get(url=Gutendex.BOOKS_ENDPOINT.replace("$", str(page))).json()

        if Gutendex.Params.results not in data:
            print(f"No Results in Page: {page}")
            return

        books = data[Gutendex.Params.results]
        print(f"Page: {page} Book Count: {len(books)}")

        p_book = Gutendex.parse_single_book(books[0])
        print(jsonpickle.encode(p_book, unpicklable=False))
