import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app import db
from app.main import bp
from app.main.forms import RecipeForm, LoginForm, RegistrationForm
from app.models import Recipe, User, Category
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', 
                         title='Home',
                         recipes=recipes)

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
        login_user(user, remember=form.remember_me_boolean.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
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

@bp.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    categories = Category.query.all()
    if not categories:
        flash('No categories available. Please contact administrator.')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        # Handle image upload
        image_url = None
        if form.image.data:
            # Create recipes directory if it doesn't exist
            recipes_dir = os.path.join(current_app.static_folder, 'images', 'recipes')
            if not os.path.exists(recipes_dir):
                os.makedirs(recipes_dir)
            
            # Save the image with a secure filename
            filename = secure_filename(form.image.data.filename)
            # Add timestamp to filename to make it unique
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            image_path = os.path.join(recipes_dir, unique_filename)
            form.image.data.save(image_path)
            
            # Store the URL path that will be accessible from the web
            image_url = url_for('static', filename=f'images/recipes/{unique_filename}')

        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            calories=form.calories.data,
            protein=form.protein.data,
            author=current_user,
            category_id=form.category.data,
            image_url=image_url,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!')
        return redirect(url_for('main.view_recipe', id=recipe.id))
    return render_template('recipe_form.html', title='New Recipe', form=form)

@bp.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('view_recipe.html', recipe=recipe)

@bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash('You can only edit your own recipes.')
        return redirect(url_for('main.view_recipe', id=id))
    form = RecipeForm()
    if form.validate_on_submit():
        # Handle image upload
        if form.image.data:
            # Create recipes directory if it doesn't exist
            recipes_dir = os.path.join(current_app.static_folder, 'images', 'recipes')
            if not os.path.exists(recipes_dir):
                os.makedirs(recipes_dir)
            
            # Save the image with a secure filename
            filename = secure_filename(form.image.data.filename)
            # Add timestamp to filename to make it unique
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            image_path = os.path.join(recipes_dir, unique_filename)
            form.image.data.save(image_path)
            
            # Store the URL path that will be accessible from the web
            recipe.image_url = url_for('static', filename=f'images/recipes/{unique_filename}')

        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        recipe.calories = form.calories.data
        recipe.protein = form.protein.data
        recipe.category_id = form.category.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        recipe.servings = form.servings.data
        db.session.commit()
        flash('Your recipe has been updated!')
        return redirect(url_for('main.view_recipe', id=id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
        form.calories.data = recipe.calories
        form.protein.data = recipe.protein
        form.category.data = recipe.category_id
    return render_template('recipe_form.html', title='Edit Recipe', form=form, recipe=recipe)

@bp.route('/recipe/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash('You can only delete your own recipes.')
        return redirect(url_for('main.view_recipe', id=id))
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted.')
    return redirect(url_for('main.index'))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, recipes=recipes)

# @bp.route('/test')
# def test():
#     return render_template('test_page.html', title='Test Page') 