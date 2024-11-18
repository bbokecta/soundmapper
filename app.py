from flask import Flask, render_template, request
from SoundMapper2 import get_more_songs 

app = Flask(__name__) 
#__name__ is a Python-reserved word, representing where the folder lives

# default_year = "2000"

default_address1 = "buckingham palace"
default_address2 = "SE173JT"
default_user_genre = "rock"

@app.route('/')
def index():
    my_playlistID = get_more_songs(default_address1, default_address2, default_user_genre)
    return render_template('index.html', address1=default_address1, address2=default_address2, genre=default_user_genre, playlist_id=my_playlistID)

@app.route('/', methods=['POST'])
def index_post():
    user_address1 = request.form['req_add1']
    user_address2 = request.form['req_add2']
    user_genre = request.form['req_genre']
    my_playlistID = get_more_songs(user_address1, user_address2, user_genre)
    # print(user_genre)
    return render_template('index.html', address1=user_address1, address2=user_address2, genre=user_genre, playlist_id=my_playlistID)