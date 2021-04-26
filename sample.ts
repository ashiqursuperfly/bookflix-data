class AuthorCreateNestedManyWithoutBooksInput {
}

class GenreCreateNestedManyWithoutBooksInput {
}

type BookCreateInput = {
    createdAt?: Date | string
    title: string
    copyright?: boolean
    language?: string
    updatedAt?: Date | string
    fileUrl: string
    fileType: string
    coverImageUrl?: string | null
    authors?: AuthorCreateNestedManyWithoutBooksInput
    genres?: GenreCreateNestedManyWithoutBooksInput
}

type AuthorCreateInput = {
    name: string
    birthYear?: number | null
    deathYear?: number | null
    createdAt?: Date | string
}

type GenreCreateWithoutBooksInput = {
    name: string
}
