from rw.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(08e9d3y$hyjt_cz(#ob93rplexio$r11x1_d7zu76adp%+qu^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
