# Fyle Accounting Mappings

## Installation and Usage

Backend infra to support all kinds of mappings in Fyle Accounting Integrations

    $ pip install fyle-accounting-mappings

In Django `settings.py` -

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    
        # Installed Apps
        'rest_framework',
        'corsheaders',
        'fyle_rest_auth', # already existing reusable django app for authentication
        'fyle_accounting_mappings', # new mapping infra app
    
        # User Created Apps
        'apps.users',
        'apps.workspaces',
        'apps.mappings',
        'apps.fyle',
        'apps.quickbooks_online',
        'apps.tasks'
    ]

Run migrations -

    $ python manage.py migrate

To use - 

    from fyle_accounting_mappings.models import MappingSetting, Mapping, ExpenseTag, DestinationTag
    
    # Operations with DB
