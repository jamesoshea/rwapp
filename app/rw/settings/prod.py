from rw.settings.base import *

DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
'/app/static/']

SECRET_KEY = '&o23hjenf0943ht98nvGASFgi#S%""/DN§F(NCQ37164'

ALLOWED_HOSTS = {
	
}