from src.models.movie import Movie
from src.models.director import Director
from src.models.actor import Actors, Actor
from src.models.genre import Genre

class Enchilada:
    def __init__(self, movie_id):
        self.movie_id = movie_id
        movie = Movie.load_by_id(movie_id)
        self.revenue = movie.revenue
        self.title = movie.title
        self.release_date = movie.release_date
        self.backdrop_path = movie.backdrop_path
        self.budget = movie.budget
        self.vote_average = movie.vote_average

        director = Director.find_by_movie_id(movie_id)
        self.director = director.name
        self.director_image = director.image

        genree = Genre.load_by_movie_id(movie_id)
        self.genre = genree

        actors = Actors.load_by_movie_id(movie_id)
        self.name0 = actors[0].name
        self.image0 = actors[0].image
        self.name1 = actors[1].name
        self.image1 = actors[1].image
        self.name2 = actors[2].name
        self.image2 = actors[2].image
        self.name3 = actors[3].name
        self.image3 = actors[3].image

    def __repr__(self):
        return "<Enchilada {}>".format(self.title)
    
    def json(self):
        return{
                'movie_id': self.movie_id,
                'revenue': self.revenue,
                'title':self.title,
                'release_date': self.release_date,
                'backdrop_path': self.backdrop_path,
                'budget': self.budget,
                'vote_average': self.vote_average,

                'director': self.director,
                'director_image': self.director_image,

                'genre': self.genre,

                'name0': self.name0,
                'image0': self.image0,
                'name1': self.name1,
                'image1': self.image1,
                'name2': self.name2,
                'image2': self.image2,
                'name3': self.name3,
                'image3': self.image3
             }