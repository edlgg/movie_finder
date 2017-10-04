from src.common.database import Database, CursorFromConnectionFromPool


class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Genre {}>".format(self.name)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO genres (id, name) VALUES (%s, %s) on conflict do nothing",(self.id, self.name))

    @classmethod
    def load_by_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM genres WHERE id=%s", (id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(id=movie_data[0], name=movie_data[1])
    @classmethod
    def load_by_movie_id(cls, movie_id):
        genres = ""
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM is_about WHERE movie_id=%s", (movie_id,))
                movie_data = cursor.fetchall()
                if movie_data:
                    for genre in movie_data[:-1]:
                        gg = Genre.load_by_id(genre[1])
                        genres += gg.name
                        genres +=  " ,"
                    gg = Genre.load_by_id(movie_data[-1][1])
                    genres += gg.name
                return genres
    
    def json(self):
        return{
                'id': self.id,
                'name': self.name
             }

    @classmethod
    def load_all(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM genres order by name")
            genres_data = cursor.fetchall()
            if genres_data:
                genres = []
                for genre in genres_data:
                    genree = Genre(genre[0], genre[1])
                    genres.append(genree.json())
                return genres


