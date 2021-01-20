import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG =True
PORT = 5000
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
LOCAL_USERNAME = "gib_dev"
LOCAL_PASSWORD = "pass1234"
TEST_DATABASE = "retailApi"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gib_dev:pass1234@localhost/retailApi"
SQLACHEMY_MIGRATE_REPO = os.path.join(basedir, "db_respository")
PAGINATION_PAGE_SIZE = 5
PAGINATION_PAGE_ARGUMENT_NAME = 'page'