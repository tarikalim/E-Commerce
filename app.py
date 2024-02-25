from create_app import create_app
# from extensions import db

app = create_app()

if __name__ == '__main__':
    # with app.app_context(): //activate those lines to create db
    #     db.create_all()

    app.run(debug=True)
