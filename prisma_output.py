class PrismaCreateAuthor:
    name: str
    birth_year: int
    death_year: int

    def __init__(self, name: str = "", birth_year: int = None, death_year: int = None) -> None:
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year


class PrismaWhere:
    name: str

    def __init__(self, name: str = None) -> None:
        self.name = name


class PrismaAuthorsConnectOrCreate:
    where: PrismaWhere
    create: PrismaCreateAuthor

    def __init__(self, where: PrismaWhere = None, create: PrismaCreateAuthor = None) -> None:
        self.where = where
        self.create = create


class PrismaAuthors:
    connect_or_create: list

    def __init__(self, connect_or_create=None) -> None:
        if connect_or_create is None:
            connect_or_create = list()
        self.connect_or_create = connect_or_create


class PrismaGenresConnectOrCreate:
    where: PrismaWhere
    create: PrismaWhere

    def __init__(self, where: PrismaWhere, create: PrismaWhere) -> None:
        self.where = where
        self.create = create


class PrismaGenres:
    connect_or_create: list

    def __init__(self, connect_or_create: list) -> None:
        self.connect_or_create = connect_or_create


class PrismaBook:
    title: str
    copyright: bool
    file_url: str
    file_type: str
    cover_image_url: str
    authors: PrismaAuthors
    genres: PrismaGenres

    def __init__(self, title: str = "", copyright: bool = False, file_url: str = "", file_type: str = "", cover_image_url: str = "", authors: PrismaAuthors = None, genres: PrismaGenres = None) -> None:
        self.title = title
        self.copyright = copyright
        self.file_url = file_url
        self.file_type = file_type
        self.cover_image_url = cover_image_url
        self.authors = authors
        self.genres = genres
