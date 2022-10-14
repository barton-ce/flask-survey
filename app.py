from flask import Flask, request, render_template, redirect, flash, session

# from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "shh-a-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route('/')
def survey_start():
    return render_template('start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def begin_survey():

    session[RESPONSES_KEY] = []

    return redirect("/questions/1")


@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:quid>")
def show_question(quid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != quid):
        flash(f'Invalid question id: {quid}.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[quid]
    return render_template("questions.html", question_num=quid, question=question)


@app.route('/complete')
def complete():
    return render_template("complete.html")
