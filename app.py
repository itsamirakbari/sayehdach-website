from flask import Flask, render_template

from config import Config
from logging_config import setup_logging
from routes.contact import contact_bp


setup_logging()


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(contact_bp)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


@app.route("/impressum")
def impressum():
    return render_template("impressum.html")


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)