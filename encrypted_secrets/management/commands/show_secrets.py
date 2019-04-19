from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.util import read_secrets

class Command(BaseCommand):
    help = 'Decrypts your application secrets and dumps them to the command line.'

    def handle(self, *args, **options):
        decrypted = read_secrets()
        print(decrypted)
