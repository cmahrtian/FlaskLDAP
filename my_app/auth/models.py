import ldap
from flask_wtf import Form
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from my_app import db, app


def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    # password = db.Column(db.String(255), nullable=False, default='')

    # User Email information
    # email = db.Column(db.String(255), nullable=False, unique=True)
    # confirmed_at = db.Column(db.DateTime())

    # User information
    # is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    # first_name = db.Column(db.String(50), nullable=False, default='')
    # last_name = db.Column(db.String(50), nullable=False, default='')

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password):
        self.username = username

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(username, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_enabled

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)