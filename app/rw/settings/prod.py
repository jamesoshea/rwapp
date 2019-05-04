import os
from rw.settings.base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#Your project will probably also have static assets that aren’t tied to a particular app.
#In addition to using a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) in your settings file where Django will also look for static files. For example:
STATICFILES_DIRS = [os.path.join(BASE_DIR, '../static')]

SECRET_KEY = '&o23hjenf0943ht98nvGASFgi#S%""/DN§F(NCQ37164'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'