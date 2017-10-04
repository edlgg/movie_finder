from src.common.database import Database, CursorFromConnectionFromPool
import json
from flask import jsonify

class Movie_Genre:
    def __init__(self, movie_id, genre_id):
        self.movie_id = movie_id
        self.genre_id = genre_id


    def __repr__(self):
        return "<movie id {} and genre id {}>".format(self.movie_id, self.genre_id)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO is_about (movie_id, genre_id) VALUES (%s, %s) on conflict do nothing",(self.movie_id, self.genre_id))

    @classmethod
    def load_by_movie_id(cls, movie_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM is_about WHERE movie_id=%s", (movie_id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(movie_id=movie_data[0], genre_id=movie_data[1])
    
    @classmethod
    def load_by_genre_id(cls, genre_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM is_about WHERE id=%s", (genre_id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(movie_id=movie_data[0], genre_id=movie_data[1])
    
    def json(self):
        return{
                'movie_id': self.movie_id,
                'genre_id': self.name,
             }


class Movie_Actors:
    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id


    def __repr__(self):
        return "<movie id {} and actor id {}>".format(self.movie_id, self.actor_id)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO acts_in (movie_id, actor_id) VALUES (%s, %s)",(self.movie_id, self.actor_id))

    @classmethod
    def load_by_movie_id(cls, movie_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM acts_in WHERE movie_id=%s", (movie_id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(movie_id=movie_data[0], actor_id=movie_data[1])
    
    @classmethod
    def load_by_actor_id(cls, actor_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM acts_in WHERE id=%s", (actor_id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(movie_id=movie_data[0], actor_id=movie_data[1])
    
    def json(self):
        return{
                'movie_id': self.movie_id,
                'actor_id': self.actor_id,
             }



