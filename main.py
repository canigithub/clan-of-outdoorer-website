from flask import Flask

from routes.main.mainpage import mainpage


app = Flask(__name__)

app.register_blueprint(mainpage)
