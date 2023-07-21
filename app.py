from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []


@app.get("/")
def home_render():
    """renders the homepage with welcome and survey instructions"""
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions
    )


@app.post("/begin")
def redirect_start():
    """clears survey response list, directs to first survey question page"""
    responses.clear()
    return redirect("/questions/0")


@app.get("/questions/<int:q_id>")
def show_question(q_id):
    """renders survey question forms"""
    question_prompt = survey.questions[q_id].prompt
    choices = survey.questions[q_id].choices

    return render_template(
        'question.html',
        question_prompt=question_prompt,
        choices=choices
    )


@app.post("/answer")
def redirect_next_question():
    """pulls response from form and adds to survey response list,
       if questions remain, direct back to survey question page,
       else direct to thank you page"""
    response = request.form["answer"]

    responses.append(response)

    if len(responses) == len(survey.questions):
        return redirect("/thank-you")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.get("/thank-you")
def show_thank_you_message():
    """renders thank you page with list of survey questions and responses"""
    questions = [prompt.prompt for prompt in survey.questions]
    response_pairs = dict(zip(questions, responses))

    return render_template(
        'completion.html',
        response_pairs = response_pairs
        )