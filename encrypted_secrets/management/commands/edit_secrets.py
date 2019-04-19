from django.core.management.base import BaseCommand, CommandError
from encrypted_secrets.util import edit_secrets

class Command(BaseCommand):
  help = 'Open secrets for editing.'

  def handle(self, *args, **options):
      edit_secrets()
