from common.database import Database, CursorFromConnectionFromPool
import json
from models.movie import Movie, Movies
import tmdbsimple as tmdb
from psycopg2 import pool
from models.relaciones import Movie_Genre, Movie_Actors
from models.director import Director
from models.actor import Actor

tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'
Database.initialize(minconn=1, maxconn=10, user="postgres", password="6627", host="localhost", database="peliculas")
"""
movies = Movies.load_all()

for movie in movies:
    moviee = tmdb.Movies(movie.id)
    response = moviee.info()
    for genre in moviee.genres:
        relation = Movie_Genre(movie.id, genre['id'])
        relation.save_to_db()


print(moviee.genres[0]['name'])
"""


movies = Movies.load_all()

for movie in movies:
    moviee = tmdb.Movies(movie.id)
    response = moviee.credits()
    for person in moviee.crew:
        if person['job'] == 'Director':
            director = Director(movie.id, person['name'], person['profile_path'])
            if not Director.load_by_movie_id(movie.id):
                director.save_to_db()

    for person in moviee.cast[:4]:
        if not Actor.load_by_movie_id(person['id']):
            actor = Actor(person['id'], person['name'], person['profile_path'])
            actor.save_to_db()
        relation = Movie_Actors(movie.id, person['id'])
        relation.save_to_db()

