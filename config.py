###################################################
### File where all needed configuration is kept ###
###################################################
import os

### Extensions needed for WTF Forms ###
WTF_CSRF_ENABLED = True			# activates the cross-site request forgery prevention
SECRET_KEY = 'a-string-which-!s-h@rd-t0-gu3$$1'

### Extensions for MySQL database ###
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data.sqlite")
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
