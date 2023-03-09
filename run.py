from app import app
import config

if __name__ == "__main__":
    if config.DEBUG == True:
        app.run(debug=True)
    else:
        app.run(debug=False)
