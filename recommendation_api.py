#recommendation_api.py

#recommendation_api.py

from flask import Flask, request, jsonify, render_template
from recommendation_engine import recommended_shows #Importing engine function
from tfidf_cosine_sim import make_tfidf_cosine_sim #Importing tfdif cosine similarity function
import pandas as pd

app = Flask(__name__)

@app.route("/")
@app.route("/input")
def hello():
    return render_template('input.html')

#Avoid switching the order of 'title' and 'confidence' keys
app.config['JSON_SORT_KEYS'] = False

drink_data = pd.read_excel('/home/ubuntu/drink_flask/static/drink.xlsx')

#API endpoint
@app.route('/api', methods=['GET', 'POST'])
def process_request():

    #Parse received JSON request
    #user_input = request.get_json()

    #Extract show drink name
    drink_name = request.form['input']

    #Get Cosine Similarity
    cos_sim = make_tfidf_cosine_sim(drink_data)

    #Call recommendation engine
    recommended_shows_dict = recommended_shows(drink_name, cos_sim, drink_data)

    return jsonify(recommended_shows_dict)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True)