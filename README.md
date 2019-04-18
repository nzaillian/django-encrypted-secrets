# django-secrets

`django-secrets` brings Rails-style [encrypted credentials](https://edgeguides.rubyonrails.org/security.html#custom-credentials) to the [Django web framework](https://www.djangoproject.com/).

## Installation

To install `django-secrets`, first pip install the module:

    $ pip install django-secrets


Add `django_secrets` to INSTALLED_APPS in your django settings file:

    INSTALLED_APPS = [
        ...
        'django_secrets'
    ]

Finally, you must call `load_secrets()` from within your `manage.py` and `wsgi.py` files:


```
#!/usr/bin/env python
import os
import sys
from django_secrets import load_secrets

if __name__ == "__main__":
    load_secrets()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourapp.settings")
    # ...
```

## Usage

Django Secrets works by using a key (stored locally in `master.key` file or read from the environment variable `DJANGO_MASTER_KEY`) and reading/writing secrets to the encrypted file `secrets.yml.enc`.

    ./manage.py init_secrets

You can edit the secrets by running:

    ./manage.py edit_secrets

When you save the file in your editor, its contents are encrypted and used to overwrite the `secrets.yml.enc` file.

Finally, to read secrets within your codebase, use the `get_secret` utility:

```
from django_secrets import get_secret

# ...

secret_api_key = get_secret("secret_api_key")

````
