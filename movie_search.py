from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from search import get_recommended_movies
from data_model import Movies
from collections import OrderedDict

DEFAULT_NUM_TO_RETURN = 100

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/movie_search.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080/"}})
db = SQLAlchemy(app)
db.init_app(app)

def validate_search_request(request_body):

    if "searchText" not in request_body:
        response = Response(response="Missing 'searchText' field", status=400)
        return True, response

    return False, None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/search', methods=['POST'])
def search():
    if request.is_json:
        body = request.json
        err, response = validate_search_request(body)
        if err:
            return response

        searchText = body["searchText"]

        if "numToReturn" in body:
            try:
                numToReturn = int(body["numToReturn"])
            except:
                msg = "'numToReturn' must be a positive integer"
                return Response(response=msg, status=400)
            if numToReturn <= 0:
                return None, 200
        else:
            numToReturn = DEFAULT_NUM_TO_RETURN
        movie_ids =  get_recommended_movies(searchText, numToReturn)
        #queryset = Movies.query.filter(Movies.movie_id.in_(movie_ids)).all()
        results_list = []
        for movie_id in movie_ids:
            movie = Movies.query.filter(Movies.movie_id == movie_id).first()
            results_list.append(movie.to_dict())
        results = {"movies": results_list}
        return results, 200

    response = Response(response="Expected json request", status=400)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')