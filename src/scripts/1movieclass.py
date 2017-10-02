import tmdbsimple as tmdb
from psycopg2 import pool
from common.database import Database, CursorFromConnectionFromPool
import json
from models.movie import Movie, Movies
tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'

Database.initialize(minconn=1, maxconn=10, user="postgres", password="6627", host="localhost", database="peliculas")

movie = tmdb.Movies(603)
response = movie.info()

moviee = Movie(movie.id, movie.revenue, movie.title, movie.release_date, movie.backdrop_path, movie.budget, movie.vote_average)
moviee.save_to_db()







