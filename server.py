# This is the python server
#  DESCRIPTION:
#       HTTP Server script that hosts until
#       canceled (Ctrl+C) on localhost on port 8000
#       once called with:
#       python3.6 server.py
#
#  MODULES USED:
#       orionsdk:    https://github.com/solarwinds/orionsdk-python
#       flask:       http://flask.pocoo.org/
#       flask-login: https://github.com/maxcountryman/flask-login
#


from flask import Flask, redirect, render_template, request, session, url_for, jsonify, current_app, send_from_directory
from os import urandom, path
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from urllib.request import urlopen
from json import loads
from datetime import date, time, datetime
import re
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
PORT = 8080
HOST = '127.0.0.1'

# login headers for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# global variables
season = ''
UPLOAD_FOLDER = 'uploads/pics/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

num_of_uploads = 0

# creates a user with an id
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

# index: first page loaded when connecting to http://localhost:8000
@app.route('/')
def index():
    # if we're not logged in, render the login page
    if not session.get('logged_in'):
        return render_template('html/login.html')
    else:
        # we're logged in, goto the dashboard funtion
        return redirect(url_for('dashboard'))

# login: page that loads when login is needed, will redirect to index
# if login fails, so that a user can reenter their credentials
# may need to implement security or logging
@app.route('/login', methods=['GET','POST'])
def login():

    # request through html
    session['username'] = request.form['username']
    session['password'] = request.form['password']

    # sql database?

    # authenticate with the server by trying a query of accounts
    if session['username'] == 'admin' and session['password'] == 'admin':
        session['logged_in'] = True
        session['invalid'] = False
        user = User(id)
        login_user(user)
    # invalid authentication
    else:
        session['invalid'] = True

    return redirect(url_for('index'))

# logout: logs a user out of the session
@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('index'))

# dashboard: this will be the main page of the dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if not session.get('logged_in'):
        return render_template('html/login.html')

    now = datetime.now()
    month = now.strftime('%b') #month

    if month == 'Mar' or month == 'Apr' or month == 'May':
        season = 'Spring'
    elif month == 'Jun' or month == 'Jul' or month == 'Aug':
        season = 'Summer'
    elif month == 'Sep' or month == 'Oct' or month == 'Nov':
        season = 'Autumn'
    elif month == 'Dec' or month == 'Jan' or month == 'Feb':
        season = 'Winter'

    return render_template('html/dashboard.html', season = season)

# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/kitchen', methods=['GET','POST'])
@login_required
def kitchen():

    return 0

# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/weather', methods=['GET','POST'])
def weather():

    
    '''
    f = urlopen('http://api.wunderground.com/api/ecbb4b84a1eafec6/geolookup/conditions/q/TN/Murfreesboro.json')
    json_string = f.read()
    parsed_json = loads(json_string)
    f.close()
    return jsonify(parsed_json)
    '''
    return 0
    
# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/scratchpad', methods=['GET','POST'])
def scratchpad():

    if request.method == 'POST':
        
        #try:
        global num_of_uploads

        # img name
        now = datetime.now()

        d = now.strftime('%d') #day
        mo = now.strftime('%b') #month
        y = now.strftime('%Y') #year
        h = now.strftime('%H') #hour
        mi = now.strftime('%M') #minute
        s = now.strftime('%S') #second
        imgname= d + mo + y + '-' + h + mi + s + '-' + str(num_of_uploads)
        print('Successfully sketch saved as ' + imgname + '!')

        # img conversion
        image_b64=request.values[('imageBase64')]
        imgstr=re.search(r'data:image/png;base64,(.*)',image_b64).group(1)  # convert
        output=open('uploads/' + y + '/' + mo + '/' + d + '/' + imgname + '.png', 'wb')
        decoded=base64.b64decode(imgstr)
        output.write(decoded)
        output.close()
        num_of_uploads += 1        # increment the global
        print('Successfully sketch saved as ' + imgname + '!')
        #except:
        #print('Could not save to server!')


    colors = ['red','orange','yellow','green','blue','indigo','violet','black','gray','white']
    return render_template('html/scratchpad.html', colors = colors)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dashboard/transfers/', methods=['GET', 'POST'])
def transfers():
    return render_template('html/filemanager.html')

@app.route('/dashboard/transfers/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('transfers',
                                    filename=filename))

@app.route('/dashboard/transfers/download/', methods=['GET', 'POST'])
def download(filename):
    if request.method == 'POST':
        uploads = path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=uploads, filename=filename)

# starts the server
if __name__ == "__main__":
    # secret key used for debugging in console/debugger
    app.secret_key = urandom(12)
    ## CHANGE THESE VALUES TO CHANGE DEBUG MODE, HOST ##
    app.run(debug=True, port=PORT, host=HOST)