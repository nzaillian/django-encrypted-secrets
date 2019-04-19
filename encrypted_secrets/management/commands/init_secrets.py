from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os
import secrets
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.util import write_secrets

ENCRYPTED_SECRETS_PATH = secrets_conf.ENCRYPTED_SECRETS_PATH

class Command(BaseCommand):
    help = 'Initialize django-encrypted-secrets install by generating a master key file.'

    def handle(self, *args, **options):
        self.key = secrets.token_urlsafe(256)
        path = f'{settings.BASE_DIR}/master.key'
        file = open(path, 'w')
        file.write(self.key)
        file.close()

        encrypted_file_exists = os.path.isfile(ENCRYPTED_SECRETS_PATH)

        if not encrypted_file_exists:
            self.write_default_encrypted_secrets_file()

    def new_file_template(self):
      message = "# Write the credentials that you want to encrypt in YAML format below.\n" \
                "# for example:\n" \
                "#\n" \
                "# aws:\n" \
                "#   access_key_id: 123\n" \
                "#   secret_access_key: 345"
      return message

    def write_default_encrypted_secrets_file(self):
          write_secrets(self.new_file_template(), self.key)
