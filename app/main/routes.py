from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app import db
from app.main import bp
from app.main.forms import LoginForm, RegistrationForm, RecipeForm
from app.models import User, Recipe, Category

@db.route('/')
def index():
    query = Recipe.query
    
    category = request.args.get('category')
    min_calories = request.args.get('min_calories')
    max_calories = request.args.get('max_calories')
    min_protein = request.args.get('min_protein')
    max_protein = request.args.get('max_protein')

    if category:
        query = query.filter(Recipe.category_id == category)
    if min_calories:
        try: 
            query = query.filter(Recipe.calories >= float(min_calories))
        except (ValueError, TypeError): 
            flash('Invalid minimum calories value')
    if max_calories:
        try: 
            query = query.filter(Recipe.calories <= float(max_calories))
        except (ValueError, TypeError):
            flash('Invalid maximum calories value')
    if min_protein: 
        try:
            query = query.filter(Recipe.protein <= float(min_protein))
        except (ValueError, TypeError):
            flash('Invalid minimum protein value')
    if max_protein: 
        try:
            query = query.filter(Recipe.protein <= float(max_protein))
        except (ValueError, TypeError):
            flash('Invalid maximum protein value')
    
    recipes = query.all()
    categories = Category.query.all()

    return render_template('index.html', title='Home', recipes=recipes, categories=categories)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me_data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)