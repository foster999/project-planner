from flask import Flask, make_response, render_template, redirect, session, request
app = Flask(__name__)

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


@app.route('/store_choice', methods=["POST"])
def store_choice():
    question_id = request.referrer.split("/")[-1]
    choice = request.form.get("choice")
    session[question_id] = choice

    next_id = request.form.get("next_id")
    next_id = None if next_id == "None" else next_id
    next_url = "/results" if next_id is None else f"/question/{next_id}"
    return redirect(next_url)


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
        question_index = question_id,
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
