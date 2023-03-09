from app import app
from config import SISTEMA_DEV

if __name__ == "__main__":
    if SISTEMA_DEV == "Windows":
        app.run()
    else:
        app.run(host="0.0.0.0")
