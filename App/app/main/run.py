from flask import Flask, url_for, send_from_directory, request, jsonify,render_template , redirect,session, flash
from flask_sqlalchemy import SQLAlchemy 
import logging, os
from werkzeug import secure_filename
from datetime import datetime
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash
import flask_login
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


#Create Flask app
app = Flask(__name__)

#Create db models
db = SQLAlchemy(app)
from  models import *



#config settings
app.secret_key = 'super secret string'  # Change this!
app.config['CORS_HEADERS'] = 'Content-Type'
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = 'C:/Users/ahemish/Downloads/nginx-1.14.2/nginx-1.14.2/html/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/ahemish/Documents/Dinners/sqlite/dinners.db'

#flask_login setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.needs_refresh_message_category = "info"


#TODO remove cors
cors = CORS(app)
    


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

#Set session length
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)



def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        
        return render_template("login.html")

    email = request.form['email']
    password= request.form['password']
    registered_user = User.query.filter_by(email_address=email).first()
    if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        
    if check_password_hash(registered_user.password, password) == True:
        flask_login.login_user(registered_user)
        flash('Logged in successfully')
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    email = request.form['email']
    password= request.form['password']
    full_name = request.form['full_name']
    username = request.form['username']
    registered_user = User.query.filter_by(email_address=email , username=username).first()
    if registered_user is None:
        new_user = User(username=username , password=generate_password_hash(password), full_name=full_name,email_address=email,created_at=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flask_login.login_user(new_user)
        return redirect(url_for('home'))
   


@app.route('/protected')
@flask_login.login_required
def protected():
 
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login')) #'Logged out'

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
@flask_login.login_required
def home():
    return render_template('index.html')


@app.route('/upload', methods = ['POST'])
@flask_login.login_required
def upload_image():
    if request.method == 'POST' and request.files['image'] and request.form['name']:
        img = request.files['image']
        name_tag = request.form['name']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        image_path = '/uploads/' + img_name
        img.save(saved_path)
        image_metadata = Image(name_tag=name_tag,image_path=image_path,image_name=img_name,created_at=datetime.now())
        db.session.add(image_metadata)
        db.session.commit()
        return 'Success' #send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:   
        return "Where is the image?"

@app.route('/allimages')
def all_images():
    image_results = Image.query.all()
    return jsonify({'results' : [{"image_id" : i.id,
    "name_tag" : i.name_tag, 
    "image_path" : i.image_path , 
    "image_name": i.image_path, 
    "created_at": i.created_at} for i in image_results]
     })

@app.route('/addfavourite')
def add_favourite():
    image_id = request.args['image_id']
    user_id = flask_login.current_user.id
    favourite = Favourite(image_id=image_id, user_id=user_id,selected_at=datetime.now())
    db.session.add(favourite)
    db.session.commit()
    return ''

@app.route('/getfavourites')
def get_favourite():
    user_id = flask_login.current_user.id
    Favourite.query.filter_by(user_id=user_id)
    return ''

@app.route('/favourites')
@flask_login.login_required
def favourites():
    return render_template('favourites.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)