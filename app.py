from creates_app import creates_app
from Route import routes
# from extensions import db

app = creates_app()
routes.init_routes(app)

if __name__ == '__main__':
    # with app.app_context(): //activate those lines to create db
    #     db.create_all()

    app.run(debug=True)
