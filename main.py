from flask import Flask

from routes.home.homeview import homeview
from routes.user.userview import userview

app = Flask(__name__)

app.secret_key = 'Copper Mountain'
app.debug = True

app.register_blueprint(homeview)
app.register_blueprint(userview)
