from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from common.database import Database, CursorFromConnectionFromPool
from models.enchilada import Enchilada
import requests
from models.movie import Movies
import json
from models.vote_average import Vote_average

Database.initialize(minconn=1, maxconn=10, user=USER, password="1ac086d22424eadccce7069b29011bd55ca5221cf6a240e249958a46969553e8", host="ec2-184-73-189-190.compute-1.amazonaws.com", database="df2bamek5iuiij", port="5432")

def function():
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM movies;");
            movies_data = cursor.fetchone()

        print(movies_data[0])

function()


