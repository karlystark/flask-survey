from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []
print('len response: ', type(len(responses)))


@app.get("/")
def home_render():
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions
    )


@app.post("/begin")
def redirect_start():
    responses.clear()
    return redirect("/questions/0")

# TODO: What question to route to next


@app.get("/questions/<int:q_id>")
def show_question(q_id):
    print('len response: ', type(len(responses)))
    question_prompt = survey.questions[q_id].prompt
    choices = survey.questions[q_id].choices

    return render_template(
        'question.html',
        question_prompt=question_prompt,
        choices=choices
    )


@app.post("/answer")
def redirect_next_question():

    response = request.form["answer"]

    responses.append(response)

    if len(responses) == len(survey.questions):
        return redirect("/Thank You!")

    else:
        return redirect(f"/questions/{len(responses)}")
