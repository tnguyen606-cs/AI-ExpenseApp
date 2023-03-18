from app import create_app

app = create_app()
app.app_context().push()

# An Alternative Way to create a debug mode
if __name__ == '__main__':
    app.run(debug=True)
