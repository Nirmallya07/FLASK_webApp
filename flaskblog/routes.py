import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm , LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required




posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if (form.gender.data == "Male") : image = "default_male.png"
        elif (form.gender.data == "Female") : image = "default_female.png"
        else : image = "952446948f7ef62dScreenshot from 2025-11-25 19-55-59.png"
        user = User(username = form.username.data, gender = form.gender.data, email = form.email.data, password = hash_pw, image_file = image)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        flash("You can now login", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')   # Need to know it better and remember this.
            flash('You have been logged in!', 'success')
            return redirect(url_for(next_page.strip("/"))) if next_page else redirect(url_for('home')) # Normal ternary operation.
            
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.split(picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    final_image = Image.open(picture)
    final_image.thumbnail(output_size)
    final_image.save(picture_path)
    # picture.save(picture_path) # A new method with pillow module is used to reduce the size of the image saved.

    return picture_fn



@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit() :
        if form.picture.data :
            picture_file =  save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info has been updated")
        redirect(url_for('account'))
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = "profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file = image_file, form = form)