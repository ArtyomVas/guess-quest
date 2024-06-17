from flask import Flask, render_template, request, redirect, url_for, jsonify
from riddle_generator import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = validate_user(username, password)
        if check is True:
            return redirect(url_for('riddle'))
        elif check != "":
            return render_template('login.html', error=check)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        print(confirm_password)
        print(password)
        if password != confirm_password:
            print("dont match")
            return render_template('signup.html', error="Passwords don't match!")
        check = add_user(username, email, password)
        if check is True:
            return redirect(url_for('login'))
        elif check != "":
            return render_template('signup.html', error=check)

    return render_template('signup.html')

@app.route('/riddle')
def riddle():
    riddle_dict = get_collection("riddleOfTheDay")
    hints = riddle_dict['hints']
    return render_template('riddle.html', hint1=hints[0], hint2=hints[1], hint3=hints[2], hint4=hints[3])

@app.route('/check_user_answer', methods=['POST'])
def check_user_answer():
    user_answer = request.form['answer']
    correct = is_valid_number(user_answer)
    return jsonify(correct=correct)


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
    app.run(host='0.0.0.0', debug=True)