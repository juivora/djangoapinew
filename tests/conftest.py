import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djangoapitest',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'djangoapi.cibpn3jdwxjv.ap-south-1.rds.amazonaws.com',
            'PORT': '5432',
        }
    }
