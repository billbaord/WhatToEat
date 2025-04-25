from app import create_app, db
from app.models import User, Recipe, Category

app = create_app()

if __name__ == '__main__':
    app.run(port=5000)  # Set default port to 5000

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Recipe': Recipe,
        'Category': Category
    } 