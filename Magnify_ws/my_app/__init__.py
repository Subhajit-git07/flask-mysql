from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_mysqldb import MySQL

from flask_compress import Compress
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
    }
 
app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html','text/css','application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

app.config.from_mapping(config)
cache = Cache(app)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'jenkins'
app.config['MYSQL_PASSWORD'] = 'ariba'
app.config['MYSQL_DB'] = 'ariba_logs'
mysql = MySQL(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
#app.config['LDAP_PROVIDER_URL'] = 'ldap://ds1phl0100.global.corp.sap:389/'
app.config['LDAP_PROVIDER_URL'] = 'ldaps://10.3.152.145:636/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from my_app.auth.views import auth
from my_app.Report_API.views2 import report
from my_app.fetch_anomaly_API.fetch_anomaly_view import Fetch_anomaly
from my_app.fetch_anomaly_count_API.fetch_anomaly_count_view import Fetch_anomaly_count
from my_app.update_anomaly_API.update_anomaly_view import Update_anomaly
from my_app.fetch_new_anomaly_relations_API.fetch_new_anomaly_relations_view import Fetch_new_anomaly_relations
from my_app.error_dictionary_API.error_dictionary_view import Error_dictionary
from my_app.update_error_dictionary_API.update_error_dictionary_view import Update_error_dictionary
from my_app.errors_count_API.errors_count_view import Errors_count
from my_app.logged_errors_API.logged_errors_view import Logged_errors
from my_app.noise_count_API.noise_count_view import Noise_count
from my_app.noise_error_count_API.noise_error_count_view import Noise_error_count
from my_app.add_to_noise_API.add_to_noise_view import Add_to_noise




app.register_blueprint(auth)
app.register_blueprint(report)
app.register_blueprint(Fetch_anomaly)
app.register_blueprint(Fetch_anomaly_count)
app.register_blueprint(Update_anomaly)
app.register_blueprint(Fetch_new_anomaly_relations)
app.register_blueprint(Error_dictionary)
app.register_blueprint(Update_error_dictionary)
app.register_blueprint(Errors_count)
app.register_blueprint(Logged_errors)
app.register_blueprint(Noise_count)
app.register_blueprint(Noise_error_count)
app.register_blueprint(Add_to_noise)


 
db.create_all()