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
        'fyle_mapping_infra', # new mapping infra app
    
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

    from fyle_mappings_infra.models import MappingSetting, Mapping, ExpenseTag, DestinationTag
    
    # Operations with DB
