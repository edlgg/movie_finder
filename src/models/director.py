from common.database import Database, CursorFromConnectionFromPool

class Director:
    def __init__(self, movie_id, name, image):
        self.movie_id = movie_id
        self.name = name
        self.image = image

    def __repr__(self):
        return "<Director>".format(self.name)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO directors (movie_id, name, image) VALUES (%s, %s, %s)",(self.movie_id, self.name, self.image))

    @classmethod
    def find_by_movie_id(cls, movie_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM directors WHERE movie_id=%s", (movie_id,))
                director = cursor.fetchone()
                if director:
                    return cls(movie_id=director[0], name=director[1], image=director[2])
    
    
    
    def json(self):
        return{
                'movie_id': self.movie_id,
                'name': self.name,
                'image':self.image
             }
    

class Directors:

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return{
                'name': self.name
             }

    @classmethod
    def load_all_list_name(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT distinct name FROM directors")
            directors_data = cursor.fetchall()
            if directors_data:
                directors = []
                for director in directors_data:
                    directors.append(director[0])
                return directors   