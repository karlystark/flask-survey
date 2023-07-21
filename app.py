from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


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
    session["responses"] = []
    return redirect("/questions/0")


@app.get("/questions/<int:q_id>")
def show_question(q_id):
    """renders survey question forms"""

    responses = session["responses"]

    if q_id != len(responses):
        #is trying to access questions out of order
        flash(f"you are attempting to access an invalid question: {q_id}")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) == len(survey.questions):
        #has reached end of survey
        return redirect("/thank-you")

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
    choice = request.form["answer"]

    #append each choice/response to the session
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    #redirect based on lengths of session responses and questions
    if len(session["responses"]) == len(survey.questions):
        return redirect("/thank-you")

    else:
        return redirect(f"/questions/{len(session['responses'])}")


@app.get("/thank-you")
def show_thank_you_message():
    """renders thank you page with list of survey questions and responses"""
    questions = [prompt.prompt for prompt in survey.questions]
    response_pairs = dict(zip(questions, session["responses"]))

    return render_template(
        'completion.html',
        response_pairs = response_pairs
        )