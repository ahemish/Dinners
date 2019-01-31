from flask import Flask, url_for, send_from_directory, request, jsonify,render_template , redirect,session, flash
from flask_sqlalchemy import SQLAlchemy 
import logging, os
from werkzeug import secure_filename
from datetime import datetime
from werkzeug.security import generate_password_hash
import flask_login
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc



#Create Flask app
app = Flask(__name__)

#Create db models
db = SQLAlchemy(app)
from  models import *



#config settings
app.config.from_pyfile('config.cfg')
app.secret_key = 'super secret string'  # Change this!
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))


#flask_login setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.needs_refresh_message_category = "info"





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
   




@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

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
        img_name = secure_filename(img.filename) + str(datetime.now().strftime("%H%M%S%f"))
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        image_path = app.config['IMAGE_PATH'] + '/' + img_name
        img.save(saved_path)
        image_metadata = Image(name_tag=name_tag,image_path=image_path,image_name=img_name,created_at=datetime.now())
        db.session.add(image_metadata)
        db.session.commit()
        return jsonify({'status':'Success'})
    else:   
        return jsonify({'status':'Failed'})

@app.route('/removedinner', methods = ['POST'])
@flask_login.login_required
def remove_image():
    if request.method == 'POST' and request.files['image'] and request.form['name']:
        image_id = request.form['image_id']
        img_name = secure_filename(img.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        remove_file(file_path)
        image_path = app.config['IMAGE_PATH'] + '/' + img_name
        image_metadata = Image(name_tag=name_tag,image_path=image_path,image_name=img_name,created_at=datetime.now())
        db.session.add(image_metadata)
        db.session.commit()
        return jsonify({'status':'Success'})
    else:   
        return jsonify({'status':'Failed'})


@app.route('/allimages')
@flask_login.login_required
def all_images():
    image_results = Image.query.order_by(desc(Image.created_at)).all()
    return jsonify({'results' : [{"image_host" : app.config['HOST'],
    "image_id" : i.id,
    "name_tag" : i.name_tag, 
    "image_path" : i.image_path , 
    "image_name": i.image_path, 
    "created_at": i.created_at} for i in image_results]
     })

@app.route('/addfavourite')
@flask_login.login_required
def add_favourite():
    image_id = request.args['image_id']
    user_id = flask_login.current_user.id
    favourite = Favourite(image_id=image_id, user_id=user_id,selected_at=datetime.now())
    db.session.add(favourite)
    db.session.commit()
    return jsonify({'status':'Success'})

@app.route('/getfavourites')
@flask_login.login_required
def get_favourite():
    user_id = flask_login.current_user.id
    favourite_images = db.session.query(Favourite,Image).filter_by(user_id=user_id).order_by(desc(Favourite.selected_at)).join(Image,Favourite.image_id==Image.id).all()
    return jsonify({'results' : [{"image_host" : app.config['HOST'],
    "image_id" : i[1].id,
    "name_tag" : i[1].name_tag, 
    "image_path" : i[1].image_path , 
    "image_name": i[1].image_path, 
    "created_at": i[1].created_at} for i in favourite_images]
     })

@app.route('/favourites')
@flask_login.login_required
def favourites():
    return render_template('favourites.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
