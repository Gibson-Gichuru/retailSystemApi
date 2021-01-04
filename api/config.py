import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG ==True
PORT = 5000
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATION = False
LOCAL_USERNAME = "gib_dev"
LOCAL_PASSWORD = "pass1234"
TEST_DATABASE = "retailApi"
SQLALCHEMY_DATABASE_URI = "pymysql+mysql://{}:{}@{}/{}".format(LOCAL_USERNAME,
	LOCAL_PASSWORD, TEST_DATABASE)
SQLACHEMY_MIGRATE_REPO = os.path.join(basedir, "db_respository")