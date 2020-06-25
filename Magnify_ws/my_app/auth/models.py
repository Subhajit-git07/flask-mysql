import ldap
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from my_app import db, app
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    # conn = ldap.initialize('ldap://10.48.176.4:389/')
    return conn
 
# conn = get_ldap_connection()
# print(conn)
# conn.simple_bind_s('cn=I503867,ou=Identities,dc=global,dc=corp,dc=sap','')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    print(username)
    def __init__(self, username, password):
        self.username = username
 
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        #'cn=%s,ou=Identities,dc=global,dc=corp,dc=sap' % username,
        try:
            result = conn.bind_s(
                'CN= %s,OU=I,OU=Identities,DC=global,DC=corp,DC=sap' %
                username,
                password
            )
        except BaseException as be:
            print("Error authenticating with the initial check")
            print(be)
            result = conn.bind_s(
                'CN= %s,OU=C,OU=Identities,DC=global,DC=corp,DC=sap' %
                username,
                password
            )
    def is_authenticated(self):
        print("called is_authenticated")
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id).encode("utf-8")
 
 
class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
