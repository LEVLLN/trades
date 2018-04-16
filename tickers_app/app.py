from flask import Flask
from models import Stock

PORT = 8080
app = Flask(__name__)
@app.route('/')
def main():
    return "fffff"

if __name__ == "__main__":
    app.run(port=PORT)
