#원래 drink_flask.py

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


# 메인 페이지 라우팅
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('choose'))
    return render_template('index.html')

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        if request.form['action'] == 'first':
            return redirect(url_for('first'))

        elif request.form['action'] == 'first2':
            return redirect(url_for('first2'))

    return render_template('choose.html')

@app.route('/first', methods=['GET', 'POST'])
def first():
    if request.method == 'POST':
        result = request.form
        return render_template('second.html', result = result)
        # return redirect(url_for('second'))
    return render_template('first.html')

@app.route('/first2', methods=['GET', 'POST'])
def first2():
    if request.method == 'POST':
        result = request.form
        return render_template('second.html', result = result)
        # return redirect(url_for('second'))
    return render_template('first2.html')

@app.route('/second', methods=['GET', 'POST'])
def second():
    if request.method == 'POST':
        return redirect(url_for('third'))
    return render_template('second.html')

@app.route('/third', methods=['GET', 'POST'])
def third():
    if request.method == 'POST':
        return redirect(url_for('fourth'))
    return render_template('third.html')

@app.route('/fourth', methods=['GET', 'POST'])
def fourth():
    if request.method == 'POST':
        return redirect(url_for('result'))
    return render_template('fourth.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    # Flask service start
    app.run(host='0.0.0.0', port=8000, debug=True)