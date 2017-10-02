from common.database import Database, CursorFromConnectionFromPool
import json
from flask import jsonify
import tmdbsimple as tmdb

class Movie:
    def __init__(self, id, revenue, title, release_date, backdrop_path, budget, vote_average):
        self.id = id
        self.revenue = revenue
        self.title = title
        self.release_date = release_date
        self.backdrop_path = backdrop_path
        self.budget = budget
        self.vote_average = vote_average

    def __repr__(self):
        return "<Movie {}>".format(self.title)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO movies (id, revenue, title, release_date, backdrop_path, budget, vote_average) VALUES (%s, %s, %s, %s, %s, %s, %s) on conflict do nothing",(self.id, self.revenue, self.title, self.release_date, self.backdrop_path, self.budget, self.vote_average))

    @classmethod
    def load_by_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM movies WHERE id=%s", (id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(id=movie_data[0], revenue=movie_data[1], title=movie_data[2], release_date=movie_data[3], backdrop_path=movie_data[4], budget=movie_data[5], vote_average=movie_data[6])
    
    def json(self):
        return{
                'id': self.id,
                'revenue': self.revenue,
                'title': self.title,
                'release_date': self.release_date,
                'backdrop_path': self.backdrop_path,
                'budget': self.budget,
                'vote_average': self.vote_average
             }
    


class Movies:
    def __init__(self):
        pass
    
    @classmethod
    def load_all(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM movies")
                movies_data = cursor.fetchall()
                if movies_data:
                    movies = []
                    for movie in movies_data:
                        new_movie = Movie(movie[0],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6],)
                        movies.append(new_movie)
                    return movies
    
    
    @classmethod
    def load_all_json_list(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM movies")
                movies_data = cursor.fetchall()
                if movies_data:
                    movies = []
                    for movie in movies_data:
                        new_movie = Movie(movie[0],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6])
                        movies.append(new_movie.json())
                    return movies
    
    @classmethod
    def load_certain_json_list(cls, actor, director, genre, sort_by):
        with CursorFromConnectionFromPool() as cursor:
                if sort_by == "Presupuesto":
                    cursor.execute("select distinct movies.id, revenue, title, release_date, backdrop_path, budget, vote_average from movies inner join directors on movies.id = directors.movie_id inner join acts_in on acts_in.movie_id = movies.id inner join actors on actors.id = acts_in.actor_id inner join is_about on is_about.movie_id = movies.id inner join genres on genres.id = is_about.genre_id where actors.name like %s and directors.name like %s and genres.name like %s order by budget desc",( actor, director, genre))
                elif sort_by == "Ingresos":
                    cursor.execute("select distinct movies.id, revenue, title, release_date, backdrop_path, budget, vote_average from movies inner join directors on movies.id = directors.movie_id inner join acts_in on acts_in.movie_id = movies.id inner join actors on actors.id = acts_in.actor_id inner join is_about on is_about.movie_id = movies.id inner join genres on genres.id = is_about.genre_id where actors.name like %s and directors.name like %s and genres.name like %s order by revenue desc",( actor, director, genre))
                else:
                    cursor.execute("select distinct movies.id, revenue, title, release_date, backdrop_path, budget, vote_average from movies inner join directors on movies.id = directors.movie_id inner join acts_in on acts_in.movie_id = movies.id inner join actors on actors.id = acts_in.actor_id inner join is_about on is_about.movie_id = movies.id inner join genres on genres.id = is_about.genre_id where actors.name like %s and directors.name like %s and genres.name like %s order by vote_average desc",( actor, director, genre))
                movies_data = cursor.fetchall()
                movies = []
                if movies_data:
                    for movie in movies_data:
                        new_movie = Movie(movie[0],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6])
                        movies.append(new_movie.json())
                    return movies
    
    @classmethod
    def create_movies(cls):
        tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'
        for i in range(1,26,1):
            discover = tmdb.Discover()
            response = discover.movie(page=i, sort_by='popularity.desc')
            for s in discover.results:
                movie = tmdb.Movies(s['id'])
                response = movie.info()
                moviee = Movie(movie.id, movie.revenue, movie.title, movie.release_date, movie.backdrop_path, movie.budget, movie.vote_average)
                moviee.save_to_db()
