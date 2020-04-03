from flask import Flask
import datetime
app = Flask(__name__)

@app.route("/")
def hello():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    return "Hello World! It's {}".format(time)

if __name__ == "__main__":
    app.run()