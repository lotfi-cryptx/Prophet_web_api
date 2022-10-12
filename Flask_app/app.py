from flask import Flask
from api.auth import init_auth
from api.proph import init_prophet
from api.database import DB

app = Flask(__name__)

app.config['SECRET_KEY'] = "top secret"

db = DB()
db.add_user('test_user', 'test_pass')

init_auth(app, '/api/v1', db)
init_prophet(app, '/api/v1', db)

app.run(debug=True)

if __name__ == "__main__":
    pass
