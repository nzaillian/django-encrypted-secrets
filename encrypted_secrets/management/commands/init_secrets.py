from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os
import secrets
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.util import write_secrets

DEFAULT_YAML_PATH =  f'{secrets_conf.SECRETS_ROOT}/secrets.yml.enc'
DEFAULT_ENV_PATH =  f'{secrets_conf.SECRETS_ROOT}/secrets.env.enc'

class Command(BaseCommand):
    help = 'Initialize django-encrypted-secrets install by generating a master key file.'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Maintain secrets in YAML or env-file format. Options are "env" or "yaml" (default is yaml).')

    def handle(self, *args, **options):
        self.mode = options.get('mode', 'yaml')
        self.key = secrets.token_urlsafe(256)
        path = f'{settings.BASE_DIR}/master.key'
        file = open(path, 'w')
        file.write(self.key)
        file.close()

        if self.mode == 'env':
            encrypted_secrets_path = DEFAULT_ENV_PATH
        else:
            encrypted_secrets_path = DEFAULT_YAML_PATH

        encrypted_file_exists = os.path.isfile(encrypted_secrets_path)

        if not encrypted_file_exists:
            self.write_default_encrypted_secrets_file(encrypted_secrets_path)

    def new_yaml_file_template(self):
      message = "# Write the credentials that you want to encrypt in YAML format below.\n" \
                "# for example:\n" \
                "#\n" \
                "# aws:\n" \
                "#   access_key_id: 123\n" \
                "#   secret_access_key: 345"
      return message

    def new_env_file_template(self):
      message = "# Write the credentials that you want to encrypt in key=value format below.\n" \
                "# for example:\n" \
                "#\n" \
                "KEY_1=\"value 1\"\n" \
                "KEY_2=123"
      return message

    def write_default_encrypted_secrets_file(self, encrypted_secrets_path):
        if self.mode == 'env':
            write_secrets(self.new_env_file_template(), self.key, encrypted_secrets_path)
        else:
            write_secrets(self.new_yaml_file_template(), self.key, encrypted_secrets_path)
