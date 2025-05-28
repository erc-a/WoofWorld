from flask import Flask
from routes import community

app = Flask(__name__)

app.register_blueprint(community.bp, url_prefix='/api/community')

if __name__ == '__main__':
    app.run(debug=True)