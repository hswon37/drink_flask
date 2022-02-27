#원래 drink_flask.py

from flask import Flask, request, render_template, redirect, url_for, jsonify
from recommendation_engine import recommended_shows #Importing engine function
from tfidf_cosine_sim import make_tfidf_cosine_sim #Importing tfdif cosine similarity function
import pandas as pd
from select_db import db_connector #Importing select data in db function

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 메인 페이지 라우팅
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('choose'))
    return render_template('index.html')

# Q. 현재 술을 가지고 있나요?
@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        if request.form['action'] == 'first':
            return redirect(url_for('first'))

        elif request.form['action'] == 'first2':
            return redirect(url_for('first2'))

    return render_template('choose.html')

# YES 버튼 클릭 후(Q1. 어떤 주류를 가지고 있나요?)
@app.route('/first', methods=['GET', 'POST'])
def first():
    if request.method == 'POST':
        return redirect(url_for('second'))
    return render_template('first.html')

# NO 버튼 클릭 후 (Q1. 어떤 주류를 원하시나요?)
@app.route('/first2', methods=['GET', 'POST'])
def first2():
    if request.method == 'POST':
        return redirect(url_for('second'))
    return render_template('first2.html')

#Q2. 어떤 맛으로 즐기고 싶나요?
@app.route('/second', methods=['GET', 'POST'])
def second():
    if request.method == 'POST':
        return redirect(url_for('third'))
    return render_template('second.html')

#Q3. 원하는 술(음료) 종류가 있나요?
@app.route('/third', methods=['GET', 'POST'])
def third():
    if request.method == 'POST':
        return redirect(url_for('fourth'))
    return render_template('third.html')

#Q4. 술의 도수
@app.route('/fourth', methods=['GET', 'POST'])
def fourth():
    if request.method == 'POST':
        return redirect(url_for('result'))
    return render_template('fourth.html')

#결과 출력
@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')


#select test
@app.route('/select', methods=['GET', 'POST'])
def select():
    name = db_connector('wine', 'Red', 13) #주류이름 받기 / 와인 테스트
    #    name = db_connector('beer', ' Pale Lager   International   Premium', 5.0) #주류이름 받기 / 맥주 테스트

    if name == '()':
        return "초기 구축단계라 아직 데이터가 부족하여 추천이 불가능합니다. 추후에 다시 테스트하러 오세요!"
    else:
        #return name[3:-5] #주류 이름 따옴표 없이 출력
        #Extract show drink name
        drink_name = str(name[3:-5])

        #Get Cosine Similarity
        cos_sim = make_tfidf_cosine_sim(drink_data)

        #Call recommendation engine
        recommended_shows_dict = recommended_shows(drink_name, cos_sim, drink_data)

        return jsonify(recommended_shows_dict)


@app.route("/input")
def hello():
    return render_template('input.html')

#추천 부분
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
    # Flask service start
    app.run(host='0.0.0.0', port=8000, debug=True)