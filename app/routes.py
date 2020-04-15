from flask import render_template, redirect, request, session, url_for, flash

from app import app
from app.config import questions
from app.utils import initialise_session, restore_session, update_session_in_db


@app.route("/")
def index():
    """
    Render index page.
    """
    session["choices"] = session.get("choices") or {}
    return render_template('index.html')


@app.route('/index')
def redirect_index():
    """
    Redirect /index to /.
    """
    return redirect("/", code=301)


@app.route("/start_quiz")
def start_quiz():
    """
    Set up session and redirect to first question.
    """
    initialise_session()
    return redirect(url_for("question", question_id = 0))


@app.route("/continue", methods = ["POST"])
def continue_session():
    """
    Continue a previous session using a session hash.
    """
    session_code = request.form.get("session_code")
    if not session_code:
        flash("Please enter a valid Session ID", "error")
    try:
        restore_session(session_code)
    except:
        flash("Sorry, no session is associated with this Session ID", "error")
        return redirect(url_for("index"))
    return redirect(session["current_page"])


@app.route("/restart")
def restart_session():
    """
    Clear the session to restart the users progress.
    """
    session.clear()
    return redirect(url_for("index"))


@app.route("/question/<int:question_id>")
def question(question_id):
    """
    Render page with question and answers.
    """
    question_data = questions[question_id]
    progress = int((question_id / len(questions)) * 100)
    return render_template(
        'question.html',
        question = question_data["question"],
        choices = question_data["choices"],
        question_index = question_id,
        next_index = question_data["next_index"],
        progress = progress,
        session_id = session.get("session_id")
        )


@app.route('/store_choice', methods=["POST"])
def store_choice():
    """
    Store question choice to session. Update current page in session.
    """
    question_id = request.referrer.split("/")[-1]
    choice = request.form.get("choice")
    session["choices"][question_id] = choice
    session.modified = True

    next_question_id = request.form.get("next_id")
    next_question_id = None if next_question_id == "None" else next_question_id
    next_url = "/results" if next_question_id is None else f"/question/{next_question_id}"
    
    # Store state for recovering position in quiz
    session["current_page"] = next_url

    update_session_in_db()
    return redirect(next_url)


@app.route("/results")
def results():
    """
    Render quiz results page.
    """
    return render_template(
        'results.html',
        choices = session.get("choices"),
        session_id = session.get("session_id")
        )
