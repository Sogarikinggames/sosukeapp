from website import create_app, db
from flask_migrate import Migrate



if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
