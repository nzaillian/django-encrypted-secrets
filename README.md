# django-encrypted-secrets

`django-encrypted-secrets` brings Rails-style [encrypted credentials](https://edgeguides.rubyonrails.org/security.html#custom-credentials) to the [Django web framework](https://www.djangoproject.com/).

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

Django Secrets works by using a key (stored locally in `master.key` file or read from the environment variable `DJANGO_MASTER_KEY`) and reading/writing secrets to the encrypted file `secrets.yml.enc`.

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

## Production considerations

`django-encrypted-secrets` looks for the encrypted secrets file within the current working directory from which you execute management commands (using `os.getcwd()`). This is implicitly the project root directory. Depending on your production server configuration, `os.getcwd()` may not actully return the project root. For production, we therefore recommend you explicitly set a `DJANGO_SECRETS_ROOT` environment variable pointing to the project root to hint to `django-encrypted-secrets` where it should look for the encrypted secrets file.
