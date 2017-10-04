from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from src.common.database import Database
from models.enchilada import Enchilada
import requests
from models.movie import Movies
import json
from models.vote_average import Vote_average
from models.actor import Actor, Actors
from models.director import Director, Directors
from models.genre import Genre
import os

__author__ = "edlgg"

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = os.environ.get("SECRET_KEY")


@app.before_first_request
def init_db():
	Database.initialize(minconn=1, maxconn=10, user=os.environ.get("USER"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))

@app.route('/',methods=['GET', 'POST'])
def homepage():
    if request.method=='POST':
        actor = request.form['actor']
        director = request.form['director']
        genre = request.form['genre']
        sort_by = request.form['sort-by']
        
        if genre == "-- Genero --":
            genre = ""
        genre = "%" + genre +"%"

        actor = "%" + actor +"%"
        director = "%" + director +"%"
        
        movies = Movies.load_certain_json_list(actor, director, genre, sort_by)
        actors = json.dumps(Actors.load_all_list_name())
        directors = json.dumps(Directors.load_all_list_name())
        genres = Genre.load_all()

        return render_template("peliculas.jinja2", movies = movies, actors=actors, directors=directors, genres = genres, actor=actor)

    movies = Movies.load_all_json_list()
    actors = json.dumps(Actors.load_all_list_name())
    directors = json.dumps(Directors.load_all_list_name())
    genres = Genre.load_all()
    return render_template("peliculas.jinja2", movies = movies, actors=actors, directors=directors, genres = genres)

@app.route('/movie/<int:id>')
def pelicula(id):
    enchilada = Enchilada(id)
    vote=Vote_average.load_by_id(enchilada.vote_average)
    enchilada = enchilada.json()

    description=vote.description
    
    return render_template("pelicula.jinja2", enchilada = enchilada, description = description)

app.run(port=4995, debug=True)