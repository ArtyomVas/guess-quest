from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from riddle_generator import *
from db_manager import *
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
app.secret_key = 'secret_guessquest_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
LOGIN_COUNT = Counter('login_count', 'Total number of logins')
SIGNUP_COUNT = Counter('signup_count', 'Total number of signups')


class User(UserMixin):
    def __init__(self, username, email):
        self.id = username
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_dict(user_id)
    if user_data:
        return User(user_data['username'], user_data['email'])
    return None


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
            user = load_user(username)
            login_user(user)
            return redirect(url_for('ready'))
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


@app.route('/ready')
@login_required
def ready():
    return render_template('ready.html')


@app.route('/riddle')
@login_required
def riddle():
    riddle_dict = get_collection("riddleOfTheDay")
    riddle_id = riddle_dict['_id']
    hints = riddle_dict['hints']
    if user_has_solved_riddle(current_user.id, riddle_id):
        return redirect(url_for('riddle_scoreboard'))
    elif user_has_gaveup_riddle(current_user.id, riddle_id):
        return redirect(url_for('riddle_losers_board'))
    update_user_start_riddle(current_user.id, riddle_id)
    print(f"MDEBUG: start riddle")
    return render_template('riddle.html', hint1=hints[0], hint2=hints[1], hint3=hints[2], hint4=hints[3])


@app.route('/check_user_answer', methods=['POST'])
def check_user_answer():
    riddle_dict = get_collection("riddleOfTheDay")
    hints = riddle_dict['hints']
    user_answer = request.form['answer']
    correct = is_valid_number(user_answer, hints[0], hints[1], hints[2], hints[3])
    return jsonify(correct=correct)


@app.route('/finished')
def riddle_scoreboard():
    riddle_dict = get_collection("riddleOfTheDay")
    if not user_has_solved_riddle(current_user.id, riddle_dict['_id']):
        update_user_solved_riddle(current_user.id, riddle_dict['_id'])
        riddle_dict = get_collection("riddleOfTheDay")
    scores = riddle_dict["scores"]
    return render_template('finished.html', scores=scores)


@app.route('/gave_up')
def riddle_losers_board():
    print(f"MDEBUG: start riddle_losers_board")
    riddle_dict = get_collection("riddleOfTheDay")
    if not user_has_gaveup_riddle(current_user.id, riddle_dict['_id']):
        update_user_gaveup_riddle(current_user.id, riddle_dict['_id'])
        riddle_dict = get_collection("riddleOfTheDay")
    losers = riddle_dict["losers"]
    print(f"MDEBUG: losers - {losers}")
    number_of_solutions = riddle_dict["numberOfPossibleSolutions"]
    print(f"MDEBUG: number_of_solutions - {number_of_solutions}")
    return render_template('gave_up.html', losers=losers, number_of_solutions=number_of_solutions)


@app.route('/api/riddle')
def api_riddle():
    riddle_dict = get_collection("riddleOfTheDay")
    return jsonify(riddle_dict)


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
