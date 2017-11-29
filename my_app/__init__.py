import os
import pymssql
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

db_uri_string = 'mssql+pymssql://' + os.getenv('MSSQL_USER') +':'+ os.getenv('MSSQL_PASS') +'@'+ os.getenv('MSSQL_SERVER') +':'+ os.getenv('MSSQL_PORT') +'/'+ os.getenv('MSSQL_DB')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_string
# app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = os.getenv('LDAP_PROVIDER_URL')
# app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from my_app.auth.views import auth
app.register_blueprint(auth)

db.create_all()