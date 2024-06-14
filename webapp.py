from flask import Flask, render_template, request, redirect, url_for, jsonify
from riddle_generator import *

app = Flask(__name__)


@app.route('/')
def index():
    riddle = get_riddle_of_the_day()
    return render_template('main_page.html', riddle=riddle)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/riddle')
def riddle():
    return render_template('riddle.html')

@app.route('/check_user_answer', methods=['POST'])
def check_user_answer():
    user_answer = request.form['answer']
    correct = is_valid_number(user_answer)
    if correct:
        result = "Correct! Well done."
    else:
        result = "Incorrect. Try again!"
    riddle = get_riddle_of_the_day()
    return render_template('main_page.html', riddle=riddle, result=result)


@app.route('/finished')
def riddle_scoreboard():
    scores = get_scores()
    return render_template('finished.html', scores=scores)

@app.route('/gave_up')
def riddle_losers_board():
    losers = get_losers()
    number_of_solutions = get_number_of_riddle_solutions()
    return render_template('gave_up.html', losers=losers, number_of_solutions=number_of_solutions)

@app.route('/api/riddle')
def api_riddle():
    riddle = get_riddle_of_the_day()
    return jsonify(riddle)


if __name__ == '__main__':
    app.run(debug=True)