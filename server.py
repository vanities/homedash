# This is the python server
#  DESCRIPTION:
#       HTTP Server script that hosts until
#       canceled (Ctrl+C) on localhost on port 8000
#       once called with:
#       python3 server.py
#
#  MODULES USED:
#       flask:       http://flask.pocoo.org/
#       flask-login: https://github.com/maxcountryman/flask-login
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.




from flask import Flask, redirect, render_template, request, session, url_for, jsonify, current_app, send_from_directory, flash
from os import urandom, path, sep, walk, listdir, chown, remove, makedirs
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from urllib.request import urlopen
from json import loads
from datetime import date, time, datetime
import re
import base64
from werkzeug.utils import secure_filename
import zipfile
from pwd import getpwnam
from grp import getgrnam


app = Flask(__name__)

# secret key used for debugging in console/debugger
app.secret_key = urandom(12)

PORT = 8000
HOST = '127.0.0.1'

# login headers for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = '/var/www/hd_static/static/'
 
PICTURE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
VIDEO_EXTENSIONS = set(['webm','mp4'])
OTHER_EXTENSIONS = set(['kdbx','txt'])
AYWAS_EXTENSIONS = set(['psd','sai'])


ALLOWED_EXTENSIONS = PICTURE_EXTENSIONS | VIDEO_EXTENSIONS | OTHER_EXTENSIONS | AYWAS_EXTENSIONS

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
    def find_season(month):
        if month == 'Mar' or month == 'Apr' or month == 'May':
            return 'umbrella' # for spring
        elif month == 'Jun' or month == 'Jul' or month == 'Aug':
            return 'sun-o'
        elif month == 'Sep' or month == 'Oct' or month == 'Nov':
            return 'leaf'
        elif month == 'Dec' or month == 'Jan' or month == 'Feb':
            return 'snowflake'

    now = datetime.now()
    month = now.strftime('%b')
    season = find_season(month)


    return render_template('html/dashboard.html', season = season)

# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/kitchen', methods=['GET','POST'])
@login_required
def kitchen():

    return 0

# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/weather', methods=['GET','POST'])
def weather():

    
    
    f = urlopen('http://api.wunderground.com/api/ecbb4b84a1eafec6/geolookup/conditions/q/TN/Murfreesboro.json')
    json_string = f.read()
    parsed_json = loads(json_string.decode('utf-8'))
    f.close()
    
    
    location = parsed_json['current_observation']['display_location']['full']
    time = parsed_json['current_observation']['observation_time']
    weather = parsed_json['current_observation']['weather']
    temperature = parsed_json['current_observation']['temperature_string']
    humidity = parsed_json['current_observation']['relative_humidity']
    heat_index = parsed_json['current_observation']['heat_index_string']
    wind = parsed_json['current_observation']['wind_string']
    icon = parsed_json['current_observation']['icon_url']
    link = parsed_json['current_observation']['forecast_url']
    
    return render_template('html/weather.html',loc = location, t = time, weather = weather, 
                                           temp = temperature, hum = humidity, hi = heat_index,
                                           wind = wind, icon = icon, link = link)
    
# dashboard: this will be the main page of the dashboard
@app.route('/dashboard/scratchpad', methods=['GET','POST'])
def scratchpad():
    colors = ['red','orange','yellow','green','blue','indigo','violet','black','gray','white']

    
    if request.method == 'POST':
        
        try:
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

            # img post request
            image_b64=request.form[('imageBase64')]
            
            imgstr=re.search(r'data:image/png;base64,(.*)',image_b64).group(1) 
            
            # img name and open
            SCRATCH_FOLDER = UPLOAD_FOLDER + 'scratch/' + y + '/' + mo.lower() + '/'
            app.config['SCRATCH_FOLDER'] = SCRATCH_FOLDER
            output=open(path.join(app.config['SCRATCH_FOLDER'], imgname + '.png'), 'wb')
            
            # img decode
            decoded=base64.b64decode(imgstr)
            
            # img write and close
            output.write(decoded)
            output.close()
            
            num_of_uploads += 1        # increment the global
            print('Successfully sketch saved as ' + imgname + '!')
            return redirect(url_for('scratchpad', colors=colors, uploaded='file saved'))

        except:
            print('Could not save to server!')

    return render_template('html/scratchpad.html', colors = colors)



@app.route('/dashboard/pictures/', methods=['GET', 'POST'])
def pictures():

    filepaths = []
    for root, dirs, files in walk(path.join(app.config['UPLOAD_FOLDER'],'pics')):
        for file in files:
            filepaths.append(root.replace('/var/www/hd_static/static/','') + '/' + file)

            
    return render_template('html/pictures.html', pictures = filepaths)

@app.route('/dashboard/transfers/', methods=['GET', 'POST'])
def transfers():
    return render_template('html/filemanager.html')
    

@app.route('/dashboard/transfers/upload/', methods=['GET', 'POST'])
def upload():
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    def is_pic(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PICTURE_EXTENSIONS
    def is_vid(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VIDEO_EXTENSIONS
    def is_other(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in OTHER_EXTENSIONS
    def is_aywas(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in AYWAS_EXTENSIONS
    def save_file_in_directory(f, d):
        FOLDER = UPLOAD_FOLDER + d + '/' + y + '/' + mo.lower() + '/'
        app.config['FOLDER'] = FOLDER
        if not path.exists(app.config['FOLDER']):
            try:
                makedirs(app.config['FOLDER'])
                print('made folders: ' + app.config['FOLDER'])
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise ('cannot make directory: ' + app.config['FOLDER'])

        file.save(path.join(app.config['FOLDER'], f))
            
            
    if request.method == 'POST':
        try:
            # img name
            now = datetime.now()
            mo = now.strftime('%b') #month
            y = now.strftime('%Y') #year
            
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            for file in request.files.getlist('file'):
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if is_pic(file.filename):
                        save_file_in_directory(filename,'pics')
                    elif is_vid(file.filename):
                        save_file_in_directory(filename,'vids')
                    elif is_other(file.filename):
                        save_file_in_directory(filename,'other')
                    elif is_aywas(file.filename):
                        save_file_in_directory(filename,'aywas')

                    print(filename + ' saved!')
                    flash(filename + ' uploaded successfully!')
                
        except:
            flash(filename + ' could not be uploaded..')
            print (filename + ' could not be uploaded..')
        return redirect(url_for('transfers'))


@app.route('/dashboard/transfers/remove_file/', methods=['GET', 'POST'])
def remove_file():
    # generic find file, dirname is defaulted to upload folder, but use this how you will
    def findfile(fn, root=app.config['UPLOAD_FOLDER']):
        for root, dirs, files in walk(root):
            
            for dir_name in dirs:
                if dir_name == fn:
                    print('found folder ' + root + '/' + dir_name + '!')
                    return root + '/' + dir_name
            for file_name in files:
                if file_name == fn:
                    print('found file ' + root + '/' + file_name + '!')
                    return root + '/' + file_name
                    
        print('could not find ' + root + '/' + file_name + '...')
    
    
    if request.method == 'POST':
        try:
            file_name = request.form['remove']
            path = findfile(file_name)
            
            if path:
                try:
                    remove(path)
                except:
                    rmdir(path)
            
            print('remove ' + path + '!')
            flash(file_name + ' removed successfully!')

        except:
            print('could not remove ' + path + '..')
            flash('could not remove ' + path + '..')

        return redirect(url_for('transfers'))

@app.route('/dashboard/transfers/tree/', methods=['GET', 'POST'])
def tree():
    path_ = path.expanduser(app.config['UPLOAD_FOLDER'])
    return render_template('html/upload.html', tree=make_tree(path_))

def make_tree(path_):
    tree = dict(name=path.basename(path_), children=[])
    try: lst = listdir(path_)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = path.join(path_, name)
            if path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

# starts the server
if __name__ == "__main__":
    ## CHANGE THESE VALUES TO CHANGE DEBUG MODE, HOST ##
    app.run(debug=True, port=PORT, host=HOST)
