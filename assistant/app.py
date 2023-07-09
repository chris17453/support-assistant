from flask import Flask
from flask_jwt_extended import JWTManager
from .server import server_blueprint

app = Flask(__name__, template_folder='templates') 
app.secret_key = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
# Register the blueprint
app.register_blueprint(server_blueprint,url_prefix='/assistant')
jwt = JWTManager(app)


if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(host='0.0.0.0', port='5001')