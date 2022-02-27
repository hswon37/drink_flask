#-*- coding:utf-8 -*-
#원래 drink_flask.py

from flask import Flask, request, render_template, redirect, url_for
from recommendation_engine import recommended_shows #Importing engine function
from tfidf_cosine_sim import make_tfidf_cosine_sim #Importing tfdif cosine similarity function
import pandas as pd
from select_db import db_connector #Importing select data in db function
import insert_db_ans as ida #for answer save

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
'''
#html 입력 받은 값 저장용
global fiResult # = "" #wine or beer
global sResult #= "" #sweet or alcohol
global tResult #= "" #wine or beer
global fResult #= "" #alcohol percentage

#db 전달용
global types #= ""
global styles #= ""
global abv1 #= ""
global abv2 #= ""
'''
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
        fiResult = request.form['drink']
        #Q1 응답 처리
        ida.insert_data(1, fiResult) 
        
        return redirect(url_for('second'))
    return render_template('first.html')

# NO 버튼 클릭 후 (Q1. 어떤 주류를 원하시나요?)
@app.route('/first2', methods=['GET', 'POST'])
def first2():
    if request.method == 'POST':
        fiResult = request.form['drink']
        #Q1 응답 처리
        ida.insert_data(1, fiResult) 
        
        return redirect(url_for('second'))
    return render_template('first2.html')

#Q2. 어떤 맛으로 즐기고 싶나요?
@app.route('/second', methods=['GET', 'POST'])
def second():
    if request.method == 'POST':
        sResult = request.form['second']
        #Q2 응답 처리
        ida.insert_data(2, sResult)
         
        return redirect(url_for('third'))
    return render_template('second.html')

#Q3. 원하는 술(음료) 종류가 있나요?
@app.route('/third', methods=['GET', 'POST'])
def third():
    if request.method == 'POST':
        tResult = request.form['third']
        #Q3 응답 처리
        ida.insert_data(3, tResult) 
        
        return redirect(url_for('fourth'))
    return render_template('third.html')

#Q4. 술의 도수
@app.route('/fourth', methods=['GET', 'POST'])
def fourth():
    if request.method == 'POST':
        fResult = request.form['fourth']
        #Q4 응답 처리
        ida.insert_data(4, fResult) 
        
        return redirect(url_for('recommend'))
#        return redirect(url_for('result'))
    return render_template('fourth.html')

#결과 출력
@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

#출력용 선택지 합치기
#result = fiResult + " " + sResult + " " + tResult + " " + fResult
'''
#Q1 응답 처리
if fiResult == "wine":
  types = 'wine'
elif fiResult == "beer":
  types = 'beer'

#Q2 응답 처리
if sResult == "sweet":
  styles = 'Red' #와인 특(추후 조사 후 수정 필요)
elif sResult == "alcohol":
  styles = ' Pale Lager   International   Premium' #맥주 특(추후 조사 후 수정 필요)

#Q3 응답 처리
if tResult == "wine":
  types = 'wine'
elif tResult == "beer":
  types = 'beer'
  
#Q4 응답 처리
if fResult == "0s":
  abv1 = '0.0'
  abv2 = '5.0'
elif fResult == "5s":
  abv1 = '5.0'
  abv2 = '10.0'
elif fResult == "10s":
  abv1 = '10.0'
  abv2 = '15.0'
elif fResult == "15s":
  abv1 = '15.0'
  abv2 = '15.0'
'''
#추천 결과
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    #DB에 저장한 응답 불러오기
    #Q1
    types = ida.select_answer(1)
    #Q2
    q2 = ida.select_answer(2)
    if q2 == "sweet":
      styles = 'Red' #와인 특(추후 조사 후 수정 필요)
    elif q2 == "alcohol":
      styles = ' Pale Lager   International   Premium' #맥주 특(추후 조사 후 수정 필요)
    else:
      styles = ''
    #Q3
    types = ida.select_answer(3)
    #Q4
    q4 = ida.select_answer(4)
    if q4 == "0s":
      abv1 = '0.0'
      abv2 = '5.0'
    elif q4 == "5s":
      abv1 = '5.0'
      abv2 = '10.0'
    elif q4 == "10s":
      abv1 = '10.0'
      abv2 = '15.0'
    elif q4 == "15s":
      abv1 = '15.0'
      abv2 = '15.0'
    else:
      abv1 = ''
      abv2 = ''
    
    name = db_connector(types, styles, abv1, abv2) #실제 입력 받기 테스트
#    name = db_connector('beer', 'Red', 10.0, 15.0) #주류이름 받기 / 없는 결과 테스트
#    name = db_connector('wine', 'Red', 10.0, 15.0) #주류이름 받기 / 와인 테스트
#    name = db_connector('beer', ' Pale Lager   International   Premium', 0.0, 5.0) #주류이름 받기 / 맥주 테스트
    
    if name == '()':
        return render_template('resultB.html') 
#        return "초기 구축단계라 아직 데이터가 부족하여 추천이 불가능합니다. 추후에 다시 테스트하러 오세요!"
    else:
        #Extract show drink name
        drink_name = str(name[3:-5])
    
        #Get Cosine Similarity
        drink_data = pd.read_excel('/home/ubuntu/drink_flask/static/drink.xlsx')
        cos_sim = make_tfidf_cosine_sim(drink_data)
    
        #Call recommendation engine
        recommended_shows_dict = recommended_shows(drink_name, cos_sim, drink_data)
         
        return render_template('resultA.html', data = recommended_shows_dict)   
        
        
if __name__ == '__main__':
    # Flask service start
    app.run(host='0.0.0.0', port=8000, debug=True)