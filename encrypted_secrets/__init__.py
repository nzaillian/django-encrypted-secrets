from .util import read_secrets
from yaml import load, FullLoader

class SecretsManager():
    secrets = {}

    @staticmethod
    def load():
        secrets_yaml = read_secrets()
        if not secrets_yaml:
            return False
        secrets_object = load(secrets_yaml, Loader=FullLoader)

        if secrets_object is None:
            SecretsManager.secrets = {}
        else:
            SecretsManager.secrets = secrets_object

    @staticmethod
    def write_secrets(secrets_obj):
        SecretsManager.secrets = secrets_obj

    @staticmethod
    def get_secret(key, default=None):
        return SecretsManager.secrets.get(key, default)

def load_secrets():
    SecretsManager.load()

def get_secret(key, default=None):
    return SecretsManager.get_secret(key, default)
