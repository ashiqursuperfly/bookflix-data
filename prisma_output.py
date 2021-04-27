class PrismaCreateAuthor:
    name: str
    birthYear: int
    deathYear: int

    def __init__(self, name: str = "", birth_year: int = None, death_year: int = None) -> None:
        self.name = name
        self.birthYear = birth_year
        self.deathYear = death_year


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
    connectOrCreate: list

    def __init__(self, connect_or_create=None) -> None:
        if connect_or_create is None:
            connect_or_create = list()
        self.connectOrCreate = connect_or_create


class PrismaGenresConnectOrCreate:
    where: PrismaWhere
    create: PrismaWhere

    def __init__(self, where: PrismaWhere = None, create: PrismaWhere = None) -> None:
        self.where = where
        self.create = create


class PrismaGenres:
    connectOrCreate: list

    def __init__(self, connect_or_create=None) -> None:
        if connect_or_create is None:
            connect_or_create = list()
        self.connectOrCreate = connect_or_create


class PrismaBook:
    title: str
    copyright: bool
    fileUrl: str
    fileType: str
    coverImageUrl: str
    authors: PrismaAuthors
    genres: PrismaGenres

    def __init__(self, title: str = "", copyright: bool = False, file_url: str = "", file_type: str = "", cover_image_url: str = "", authors: PrismaAuthors = None, genres: PrismaGenres = None) -> None:
        self.title = title
        self.copyright = copyright
        self.fileUrl = file_url
        self.fileType = file_type
        self.coverImageUrl = cover_image_url
        self.authors = authors
        self.genres = genres
