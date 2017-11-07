SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "nabla_core",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
