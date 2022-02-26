#원래 drink_flask.py

from flask import Flask, render_template

app = Flask(__name__)


# ���� ������ �����
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')



if __name__ == '__main__':
    # Flask service start
    app.run(host='0.0.0.0', port=8000, debug=True)
