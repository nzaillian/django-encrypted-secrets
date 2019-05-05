from .util import read_secrets
import yaml
from yaml import load, FullLoader
import encrypted_secrets.conf as secrets_conf

class YAMLFormatException(Exception):
    pass

class SecretsManager():
    secrets = {}

    @staticmethod
    def load(encrypted_secrets_file_path=secrets_conf.ENCRYPTED_SECRETS_PATH, key=secrets_conf.ENCRYPTED_SECRETS_KEY):
        secrets_yaml = read_secrets(encrypted_secrets_file_path, key)
        if not secrets_yaml:
            return False

        try:
            secrets_object = load(secrets_yaml, Loader=FullLoader)
        except yaml.YAMLError:
            SecretsManager._raise_invalid_syntax()
        if isinstance(secrets_object, str):
            SecretsManager._raise_invalid_syntax()

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

    @staticmethod
    def _raise_invalid_syntax(error_message=None):
        raise YAMLFormatException("Invalid YAML syntax detected in secrets file. Please double-check syntax.")

def load_secrets():
    SecretsManager.load()

def get_secret(key, default=None):
    return SecretsManager.get_secret(key, default)
