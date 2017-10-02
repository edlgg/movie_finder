from common.database import Database, CursorFromConnectionFromPool
import json
from models.movie import Movie, Movies
import tmdbsimple as tmdb
from psycopg2 import pool

tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'
Database.initialize(minconn=1, maxconn=10, user="postgres", password="6627", host="localhost", database="peliculas")


## get list of movie ids
movie_ids = []
for i in range(1,26,1):
    discover = tmdb.Discover()
    response = discover.movie(page=i, sort_by='popularity.desc')
    for s in discover.results:
        movie_ids.append(s['id'])



##create movies and save
movies = []
for i in range(1,len(movies),1):
    movie = tmdb.Movies(movie_ids[i])
    response = movie.info()

    moviee = Movie(movie.id, movie.revenue, movie.title, movie.release_date, movie.backdrop_path, movie.budget, movie.vote_average)
    movies.append(moviee)
    #moviee.save_to_db()

#get movies top 3 actors
#get diretor

#get genres





    