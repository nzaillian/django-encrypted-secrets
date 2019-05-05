# django-encrypted-secrets

[![CircleCI](https://img.shields.io/circleci/project/github/nzaillian/django-encrypted-secrets/development.svg?style=popout)](https://circleci.com/gh/nzaillian/django-encrypted-secrets/tree/development) [![Django Versions](https://img.shields.io/pypi/djversions/django-encrypted-secrets.svg?style=popout)](https://www.djangoproject.com/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-encrypted-secrets.svg?color=rgb%2868%2C%20204%2C%2017%29&style=popout)](https://www.python.org)

`django-encrypted-secrets` brings [Rails-style credential encryption](https://edgeguides.rubyonrails.org/security.html#custom-credentials) to the [Django web framework](https://www.djangoproject.com/).

## Installation

To install `django-encrypted-secrets`, first pip install the module:

    $ pip install django-encrypted-secrets


Add `encrypted_secrets` to INSTALLED_APPS in your django settings file:

    INSTALLED_APPS = [
        ...
        'encrypted_secrets'
    ]

Finally, you must call `load_secrets()` from within your `manage.py` and `wsgi.py` files:


```
#!/usr/bin/env python
import os
import sys
from encrypted_secrets import load_secrets

if __name__ == "__main__":
    load_secrets()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourapp.settings")
    # ...
```

## Usage

`django-encrypted-secrets` works by using a key (stored locally in `master.key` file or read from the environment variable `DJANGO_MASTER_KEY`) and reading/writing secrets to the encrypted file `secrets.yml.enc`.

    ./manage.py init_secrets

You can edit the secrets by running:

    ./manage.py edit_secrets

When you save the file in your editor, its contents are encrypted and used to overwrite the `secrets.yml.enc` file.

Finally, to read secrets within your codebase, use the `get_secret` utility:

```
from encrypted_secrets import get_secret

# ...

secret_api_key = get_secret("secret_api_key")

````

You should always keep your `master.key` file `.gitignored`.

## env mode (experimental)

`django-encrypted-secrets` experimentally supports loading key-value pairs from an encrypted file written in the [dotenv](https://github.com/theskumar/python-dotenv) format directly into the environment. To use this style of variable loading, you must pass `env_mode=True` to your `load_secrets` call in `manage.py` and `wsgi.py`:

```
#!/usr/bin/env python
import os
import sys
from encrypted_secrets import load_secrets

if __name__ == "__main__":
    load_secrets(env_mode=True) # <- important
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourapp.settings")
    # ...
```

You must also pass the `--mode=env` flag to the `init_secrets` management command when initializing `django-encrypted-secrets`:

```
$ ./manage.py init_secrets --mode=env
```

A template encrypted dotenv-type file will be written to `secrets.env.enc`. When using env mode, secrets are automatically added to the environment. This means that, in addition to being able to read secrets using the `get_secret` helper method, you may also read them as ordinary environment variables. If an environment variable configured in the file already exists in the environment, it will *not* be overriden. This is because we assume that you may want to override variables from `django-encrypted-secrets` with environment variables set in your deployment environment.

Example of reading environment variables directly from the environment and using `get_secret`:

```
import os
from encrypted_secrets import get_secret

# option 1 - read directly from the environment:
secret_api_key = os.environ.get('SECRET_API_KEY')

# option 2 - use get_secret:
secret_api_key = get_secret('SECRET_API_KEY')
```

## Production considerations

`django-encrypted-secrets` looks for the encrypted secrets file within the current working directory from which you execute management commands (using `os.getcwd()`). This is implicitly the project root directory. Depending on your production server configuration, `os.getcwd()` may not actully return the project root. For production, we therefore recommend you explicitly set a `DJANGO_SECRETS_ROOT` environment variable pointing to the project root to hint to `django-encrypted-secrets` where it should look for the encrypted secrets file.
