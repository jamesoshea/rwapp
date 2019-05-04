import os
from rw.settings.base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
'/app/static/']

SECRET_KEY = '&o23hjenf0943ht98nvGASFgi#S%""/DN§F(NCQ37164'

ALLOWED_HOSTS = [
	'178.128.197.252'
]
