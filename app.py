from flask import Flask, render_template, request
from example_spotify import get_songs

app = Flask(__name__) 
#__name__ is a Python-reserved word, representing where the folder lives

default_year = "2000"

@app.route('/')
def index():
    my_songs = get_songs(default_year)
    return render_template('index.html', year=default_year, songs=my_songs)

@app.route('/', methods=['POST'])
def index_post():
    user_year = request.form['req_year']
    my_songs = get_songs(user_year)
    return render_template('index.html', year=user_year, songs=my_songs)