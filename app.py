"""Trivia app."""
import requests, html, random, os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("TRIVIA_APP_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def page_not_found(error):
    """404 page."""
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    """Index page."""
    session.pop('correct_count', None)
    session.pop('incorrect_count', None)
    return render_template('index.html')


class TriviaGame:
    """Trivia Game class."""

    def __init__(self):
        """Initialize the game."""
        self.correct_count = 0
        self.incorrect_count = 0
        self.result = None
        self.last_correct_answer = None

    def play(self):
        """Play the game."""
        question, answers, correct_answer = get_data()
        session['last_correct_answer'] = self.last_correct_answer

        if request.method == 'POST':
            user_answer = request.form.get('answer')
            if user_answer is not None:
                if html.unescape(user_answer) == self.last_correct_answer:
                    self.result = "Correct"
                    session['correct_count'] = session.get(
                        'correct_count', 0) + 1
                else:
                    self.result = "Incorrect"
                    session['incorrect_count'] = session.get(
                        'incorrect_count', 0) + 1
            else:
                self.result = "Please select an answer."

        else:
            self.result = None

        self.last_correct_answer = correct_answer
        self.correct_count = session.get('correct_count', 0)
        self.incorrect_count = session.get('incorrect_count', 0)

        return question, answers, self.result

    def get_answer_count(self):
        """Get the total number of answers."""
        return self.correct_count + self.incorrect_count


def get_data(amount: int = 1, category: int = 9, question_type: str = 'multiple') -> tuple:
    """Get data from the API."""
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&type={question_type}"
    response = requests.get(url)
    data_json = response.json()
    questions = data_json['results']
    data = questions[0]
    question = html.unescape(data['question'])
    correct_answer = html.unescape(data['correct_answer'])
    answers = [html.unescape(answer) for answer in data['incorrect_answers']]
    answers.append(correct_answer)
    shuffled_answers = shuffle_answers(answers)
    return question, shuffled_answers, correct_answer


def shuffle_answers(answers: list) -> list:
    """Shuffle the answers."""
    random.shuffle(answers)
    return answers


@app.route('/play', methods=['GET', 'POST'])
def play_game():
    """Game page."""
    if request.method == 'POST':
        question, answers, result = game.play()
        if result == "Please select an answer.":
            result = None
        answer_count = game.get_answer_count()
        correct_count = game.correct_count
        incorrect_count = game.incorrect_count
        return render_template('play.html', question=question, answers=answers, result=result, answer_count=answer_count, correct_count=correct_count, incorrect_count=incorrect_count)

    return redirect(url_for('index', _timestamp=random.random()))


@app.route('/about', methods=['GET', 'POST'])
def about():
    """About page."""
    return render_template('about.html')


game = TriviaGame()


if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)
