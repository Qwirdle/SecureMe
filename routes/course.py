from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *
from __main__ import app, Users, db

from util import checkAnswers
import datetime


@app.route('/home/credential/')
@login_required
def credentialText():
    return render_template('/chapters/credential/credential-text.html')

@app.route('/home/credential/quiz/', methods=["GET", "POST"])
@login_required
def credentialQuiz():

    if request.method == "POST":
        # check for correct questions
        score = checkAnswers(request.form, ("b", "a", "c", "a", "d", "a", "c", "b"))

        # redirect user to either passed or fail page, and send
        # through score/what test was taken to both page and db
        if score >= 70:
            # only commit score if passed
            user = Users.query.filter_by(username=current_user.username).first()
            user.credPass = True
            db.session.commit()

            # use render template because we don't need an actual link to an emmpty passed/failed
            return render_template('/misc/passed.html', score=round(score, 2), test="Credential")
        else:
            return render_template('/misc/failed.html', score=round(score, 2), test="Credential")

    return render_template('/chapters/credential/credential-quiz.html')

@app.route('/home/information/')
@login_required
def informationText():
    return render_template('/chapters/information/information-text.html')

@app.route('/home/information/quiz/', methods=["GET", "POST"])
@login_required
def informationQuiz():

    if request.method == "POST":
        score = checkAnswers(request.form, ("b", "d", "a", "d", "d", "a", "d", "b"))

        if score >= 70:
            user = Users.query.filter_by(username=current_user.username).first()
            user.infoPass = True
            db.session.commit()

            return render_template('/misc/passed.html', score=round(score, 2), test="Information")
        else:
            return render_template('/misc/failed.html', score=round(score, 2), test="Information")

    return render_template('/chapters/information/information-quiz.html')

@app.route('/home/malware/')
@login_required
def malwareText():
    return render_template('/chapters/malware/malware-text.html')

@app.route('/home/malware/quiz/', methods=["GET", "POST"])
@login_required
def malwareQuiz():

    if request.method == "POST":
        score = checkAnswers(request.form, ("c", "d", "a", "c", "b", "c", "a", "c"))

        if score >= 70:
            user = Users.query.filter_by(username=current_user.username).first()
            user.malPass = True
            db.session.commit()

            return render_template('/misc/passed.html', score=round(score, 2), test="Malware")
        else:
            return render_template('/misc/failed.html', score=round(score, 2), test="Malware")

    return render_template('/chapters/malware/malware-quiz.html')

# final test
@app.route('/home/final', methods=["GET", "POST"])
@login_required
def finalTest():
    user = Users.query.filter_by(username=current_user.username).first()
    if request.method == "POST":
        score = checkAnswers(request.form, ("b", "d", "c", "a", "b", "c", "b", "c", "b", "d", "b", "b", "c", "a", "c"))

        if score >= 70:
            user.finalPass = True

            # only record first date
            if user.cdate == "none":
                # normal date formatting
                user.cdate = datetime.datetime.now().strftime("%B %d, %Y")
            
            db.session.commit()

            return render_template('/misc/passed.html', score=round(score, 2), test="Final")
            
            # commit course completion date
        else:
            return render_template('/misc/failed.html', score=round(score, 2), test="Final")

    # only allow access if the user passed everything else
    if user.credPass and user.infoPass and user.malPass == True:
        return render_template('final.html')
    else:
        return render_template('home.html', credPass=user.credPass, infoPass=user.infoPass,  malPass=user.malPass, finalPass=user.finalPass)