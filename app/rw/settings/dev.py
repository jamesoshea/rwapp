from rw.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(08e9d3y$hyjt_cz(#ob93rplexio$r11x1_d7zu76adp%+qu^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
#Your project will probably also have static assets that aren’t tied to a particular app.
#In addition to using a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) in your settings file where Django will also look for static files. For example:
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
'/app/static/']
