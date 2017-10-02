from common.database import Database, CursorFromConnectionFromPool
import json
from models.movie import Movie, Movies
import tmdbsimple as tmdb
from psycopg2 import pool
from models.relaciones import Movie_Genre

tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'
Database.initialize(minconn=1, maxconn=10, user="postgres", password="6627", host="localhost", database="peliculas")

movies = Movies.load_all()

for movie in movies:
    moviee = tmdb.Movies(movie.id)
    response = moviee.info()
    for genre in moviee.genres:
        relation = Movie_Genre(movie.id, genre['id'])
        relation.save_to_db()

    