from app import create_app, db
from app.models import User, Recipe, Category

app = create_app()
app.app_context().push()

# Drop all tables
db.drop_all()

# Create all tables
db.create_all()

# Create some initial categories if they don't exist
categories = ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Snack']
for category_name in categories:
    if not Category.query.filter_by(name=category_name).first():
        category = Category(name=category_name)
        db.session.add(category)

# Create a test user if it doesn't exist
if not User.query.filter_by(username='test').first():
    user = User(username='test', email='test@example.com')
    user.set_password('test')
    db.session.add(user)

# Commit the changes
db.session.commit()

print("Database initialized successfully!") 