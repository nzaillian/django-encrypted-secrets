from .util import read_secrets, parse_env_string
import os
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
        env_string = read_secrets(encrypted_secrets_file_path, key)

        if not env_string:
            return False

        secrets_obj = parse_env_string(env_string)
        cls.secrets = secrets_obj

        # merge secrets into ENV:
        for k, v in secrets_obj.items():
            cls._merge_into_env(k, v)

    @classmethod
    def _merge_into_env(cls, key, val):
        if key not in os.environ:
            os.environ[key] = val

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
