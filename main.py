from flask import Flask, make_response, render_template, redirect, session
app = Flask(__name__)
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

choice_type = {
        "binary": ["Yes", "No"]
        }

questions = [
    {
        "question":
            "Are your outputs business critical?",
        "choices": choice_type["binary"],
        "next_index":1
        },
    {
        "question":
            "Are users of your code able to program in the appropriate"
            " language?",
        "choices": choice_type["binary"],
        "next_index": None
      }
]

default_scores = {
        "documentation": 0,
        "peer_review": 0,
        "testing": 0,
        }

def store_choice(question_id, choice):
    session[question_id] = choice

def get_results():
    return session

@app.route("/")
def index():
    session.clear()
    return make_response(render_template('index.html'), 200)

@app.route('/index')
def redirect_index():
    return redirect("/", code=301)

@app.route("/question/<int:question_id>")
def question(question_id):
    question_data = questions[question_id]
    progress = int((question_id / len(questions)) * 100)
    return render_template(
        'question.html',
        question = question_data["question"],
        choices = question_data["choices"],
        next_index = question_data["next_index"],
        progress = progress
        )

@app.route("/results")
def results():
    return render_template(
        'results.html',
        session = session
        )

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run()
