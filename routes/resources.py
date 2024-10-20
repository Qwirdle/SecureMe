from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *
from __main__ import app, Users, db

@app.route('/resources/tools')
# login required integrates blocked part of page with login_manager
@login_required
def toolsApps():
    return render_template('/resources/tools-apps.html')

@app.route('/resources/media')
@login_required
def podcastsMedia():
    return render_template('/resources/podcast-media.html')

@app.route('/resources/educational')
@login_required
def education():
    return render_template('/resources/educational.html')