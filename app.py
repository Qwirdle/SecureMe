from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *

from cert import genCert

import os

app = Flask(__name__)
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# GEN A SECRET KEY (https://randomkeygen.com/)
app.config["SECRET_KEY"] = ""
# init
db = SQLAlchemy()

# enable csrf protection
csrf = CSRFProtect(app)

# login manager handles
login_manager = LoginManager()
login_manager.init_app(app)

# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    
    # scores for each test ( change to bool )
    credPass = db.Column(db.Boolean, default=False)
    infoPass = db.Column(db.Boolean, default=False)
    malPass = db.Column(db.Boolean, default=False)
    finalPass = db.Column(db.Boolean, default=False)

    fname = db.Column(db.String(250),
                         nullable=False)
    lname = db.Column(db.String(250),
                         nullable=False)
    
    cdate = db.Column(db.String(250),
                         default="none")

# init rest of appp
db.init_app(app)
 
with app.app_context():
    db.create_all()

# func to load in user
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


# import app elements
import routes.login
import routes.course
import routes.resources


@app.route('/home/')
# login required integrates blocked part of page with login_manager
@login_required
def home():
    # go through each db assignment score and see if it has been passed
    user = Users.query.filter_by(username=current_user.username).first()
    
    return render_template('home.html', credPass=user.credPass, infoPass=user.infoPass,  malPass=user.malPass, finalPass=user.finalPass)

# for testing, remove later
@app.route('/certification')
@login_required
def certification():
    user = Users.query.filter_by(username=current_user.username).first()
    if all((user.credPass, user.infoPass, user.malPass, user.finalPass)):
        # generate a certification using user data
        tpl = genCert(f"{user.fname} {user.lname}", user.cdate)
        tpl.save(f"{os.getcwd()}/certs/{user.username}_cert.docx")

        # send through browser download
        return send_file(f"{os.getcwd()}/certs/{user.username}_cert.docx", as_attachment=True)


    return render_template('home.html', credPass=user.credPass, infoPass=user.infoPass,  malPass=user.malPass, finalPass=user.finalPass)


# logout
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index"))

# redirect to index when accessing unauthorized part of site
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))

if __name__ == "__main__":
    # disable debug when deploying
    app.run(debug=True)