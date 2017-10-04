from common.database import Database
from models.movie import Movies, Movie
from models.actor import Actor, Actors
from models.director import Director
from models.relaciones import Movie_Actors, Movie_Genre
import tmdbsimple as tmdb
from private import MDB_API_KEY

#Database.initialize(minconn=1, maxconn=10, user="postgres", password="", host="localhost", database="peliculas2")
Database.initialize(minconn=1, maxconn=10, user=os.environ.get("USER"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))


tmdb.API_KEY = MDB_API_KEY

def create_actors_acts_in_and_directors():
    movies = Movies.load_all()

    for movie in movies:
        moviee = tmdb.Movies(movie.id)
        response = moviee.credits()
        for person in moviee.crew:
            if person['job'] == 'Director':
                director = Director(movie.id, person['name'], person['profile_path'])
                if not Director.find_by_movie_id(movie.id):
                    director.save_to_db()

        for person in moviee.cast[:4]:
            if not Actor.load_by_id(person['id']):
                actor = Actor(person['id'], person['name'], person['profile_path'])
                actor.save_to_db()
            relation = Movie_Actors(movie.id, person['id'])
            relation.save_to_db()

def create_is_about():
        movies = Movies.load_all()

        for movie in movies:
            moviee = tmdb.Movies(movie.id)
            response = moviee.info()
            for genre in moviee.genres:
                relation = Movie_Genre(movie.id, genre['id'])
                relation.save_to_db()


#Database.create_tables() #Creates databases; populate genres and vote_averages
#Movies.create_movies()
#create_actors_acts_in_and_directors()
create_is_about()
