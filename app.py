from flask import Flask, render_template, request, redirect, url_for, jsonify
from riddler import *

app = Flask(__name__)


@app.route('/')
def index():
    riddle = create_a_riddle()
    return render_template('index.html', riddle=riddle)


@app.route('/check_user_answer', methods=['POST'])
def check_user_answer():
    user_answer = request.form['answer']
    correct = check_answer(user_answer)
    if correct:
        result = "Correct! Well done."
    else:
        result = "Incorrect. Try again!"
    riddle = create_a_riddle()
    return render_template('index.html', riddle=riddle, result=result)


@app.route('/riddle_scoreboard')
def riddle_scoreboard():
    return render_template('riddle_scoreboard.html')

@app.route('/api/riddle')
def api_riddle():
    riddle = create_a_riddle()
    return jsonify(riddle)


if __name__ == '__main__':
    app.run(debug=True)