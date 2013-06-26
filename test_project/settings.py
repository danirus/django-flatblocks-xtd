import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

DEBUG=True
TEMPLATE_DEBUG=True

DATABASES = {
    'default': {
        'ENGINE':   "django.db.backends.sqlite3",
        'NAME':     "flatblocks_xtd.db",
        'USER':     "", 
        'PASSWORD': "", 
        'HOST':     "", 
        'PORT':     "",
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

STATIC_URL = "/static/"

SECRET_KEY = 'v2824l&2-n+4zznbsk9c-ap5i)b3e8b+%*a=dxqlahm^%)68jn'

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'tagging',
    'inline_media',
    'flatblocks_xtd',
)

LANGUAGE_CODE="en"
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
ROOT_URLCONF = 'test_project.urls'

THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"
THUMBNAIL_FORMAT = "JPEG"

# ADMIN_IMAGES_PATH = "%s/admin/img/admin" % STATIC_URL # Django 1.3

INLINE_MEDIA_TEXTAREA_ATTRS = {
    'default': { # default widget attributes, can be overriden on
                 # a per app_label.model basis
        'style': 'font: 12px monospace'
    },
    'flatblocks_xtd.flatblock_xtd': { # widget attributes for app_label.model
        'content': { 'rows': 20 } # field 'body'
    }
}

INLINE_MEDIA_CUSTOM_SIZES = {
    'inline_media.picture':    { 'large': 310 },
    'inline_media.pictureset': { 'large': (288, 240) }
}
