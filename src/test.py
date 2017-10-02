from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from common.database import Database
from models.enchilada import Enchilada
import requests
from models.movie import Movies
import json
from models.vote_average import Vote_average

Database.initialize(minconn=1, maxconn=10, user="postgres", password="6627", host="localhost", database="peliculas")

movies = Movies.load_certain_json_list("Samuel L. Jackson", "Quentin Tarantino", "Thriller", "vote_average")

print(movies)