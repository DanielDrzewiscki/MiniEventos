"""
Django settings for ProyectoWeb project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from decouple import config

import os


from django.contrib.messages import constants as mensaje_de_error

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '6nhhvwvki5-a)&f+mdfkj4e=mx8b^&*k01*e4(r6shuwe1ml#='
SECRET_KEY =config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG =config('DEBUG')

#ALLOWED_HOSTS = []

ALLOWED_HOSTS = [
  'localhost',
  '127.0.0.1',
  '192.168.0.212',
  'sigev.linkpc.net',
  'sigev.publicvm.com',
  'minieventos.linkpc.net']



# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'Aplicacion1',
    'servicios',
    'blog',
    'contacto',
    'tienda',
    'carro',
    'autenticacion',
    'crispy_forms',
    'pedidos',
    'ubicacion',
    'quienessomos',
    'galeria',
    'usuarios',
    'administracion',
    'colorfield',
    'sql_server.pyodbc',
    
]

X_FRAME_OPTIONS = "SAMEORIGIN"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProyectoWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'carro.context_processor.importe_total_carro',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


#Configuracion para SQLite
#DATABASES = {
#    'default': {
#        'ENGINE': config('DATABASES_URL'),
#        'NAME': BASE_DIR / config('DATABASE_NAME'),
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': config('DATABASES_URL'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': '',
        'OPTIONS': {
            'drivers': config('DATABASE_DRIVERS'),
            
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-eu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/




STATIC_URL = '/static/'
STATIC_ROOT= BASE_DIR / 'static'

# Definimos la ruta donde django debe poner y buscar los archivos
# multimedia (En este caso ya hemos creado la carpeta "media" en la raiz del proyecto)

MEDIA_URL= '/media/'
MEDIA_ROOT= BASE_DIR / 'media'


#Configuracion del servidor de Mail de Gmail

#EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST='smtp.gmail.com'
#EMAIL_USE_TLS=True
#EMAIL_PORT=587
#EMAIL_HOST_USER="daniel.drzewiscki@gmail.com"
#EMAIL_HOST_PASSWORD="xzthbmoanbjflfjh"

EMAIL_BACKEND=config('EMAIL_BACKEND')
EMAIL_HOST=config('EMAIL_HOST')
EMAIL_USE_TLS=config('EMAIL_USE_TLS')
MAIL_PORT=config('EMAIL_PORT')
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')


CRISPY_ALLOWED_TEMPLATE_PACK='bootstrap4'
CRISPY_TEMPLATE_PACK='bootstrap4'

MESSAGE_TAGS = {

    mensaje_de_error.DEBUG: 'debug',
    mensaje_de_error.INFO: 'info',
    mensaje_de_error.SUCCESS: 'success',
    mensaje_de_error.WARNING: 'warning',
    mensaje_de_error.ERROR: 'danger',

}
