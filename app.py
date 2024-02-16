from creates_app import creates_app
from Model.models import db
from Route import routes

app = creates_app()
routes.init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
