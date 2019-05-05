from .util import read_secrets
import yaml
from yaml import load, FullLoader
import encrypted_secrets.conf as secrets_conf

class YAMLFormatException(Exception):
    pass

class SecretsManager():
    secrets = {}
    mode = 'yaml'

    @classmethod
    def load(cls, encrypted_secrets_file_path=secrets_conf.ENCRYPTED_SECRETS_PATH, key=secrets_conf.ENCRYPTED_SECRETS_KEY, **kwargs):
        if kwargs.get('env_mode') == True:
            cls.mode = 'env'

        if cls.mode == 'yaml':
            cls.load_from_yaml(encrypted_secrets_file_path, key)
        elif cls.mode == 'env':
            cls.load_from_env_file(encrypted_secrets_file_path, key)

    @classmethod
    def load_from_yaml(cls, encrypted_secrets_file_path, key):
        secrets_yaml = read_secrets(encrypted_secrets_file_path, key)
        if not secrets_yaml:
            return False

        try:
            secrets_object = load(secrets_yaml, Loader=FullLoader)
        except yaml.YAMLError:
            cls._raise_invalid_syntax()
        if isinstance(secrets_object, str):
            cls._raise_invalid_syntax()

        if secrets_object is None:
            cls.secrets = {}
        else:
            cls.secrets = secrets_object

    @classmethod
    def load_from_env_file(cls, encrypted_secrets_file_path, key):
        pass

    @classmethod
    def write_secrets(cls,secrets_obj):
        cls.secrets = secrets_obj

    @classmethod
    def get_secret(cls, key, default=None):
        return cls.secrets.get(key, default)

    @staticmethod
    def _raise_invalid_syntax(error_message=None):
        raise YAMLFormatException("Invalid YAML syntax detected in secrets file. Please double-check syntax.")

def load_secrets(**kwargs):
    SecretsManager.load(**kwargs)

def get_secret(key, default=None):
    return SecretsManager.get_secret(key, default)
