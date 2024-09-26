from app import create_app

app = create_app()

# make sure to run using python run.py and not flask start
if __name__ == "__main__":
    app.run(debug=True)