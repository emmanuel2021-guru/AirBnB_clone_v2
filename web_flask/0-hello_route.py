from flask import Flask

hello = Flask(__name__)

@hello.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"
if __name__ == "__main__":
    hello.run(host='0.0.0.0', port=5000)
