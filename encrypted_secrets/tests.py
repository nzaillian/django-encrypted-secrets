import os, glob
from yaml import load, FullLoader
from django.test import TestCase
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.util import *
from encrypted_secrets import SecretsManager, get_secret, YAMLFormatException

ROOT = os.getcwd()
TMP_PATH = f'{ROOT}/test_tmp'
TEST_KEY = "oq-KteLds9DXGLh30y_eGw0nE4fLGUbtkXA3YppItmuZgNlyiw264BViP14lOxg_X8e8vLx6K4KABbOnDwGzQCPHcLuidS-EwF2uJCtK-qWVaaZ9USoHjcyEp1LAPVvAfiLQ3q_xY0DWJGDtBPYJdREg44Qiu1AVFsI46QlJESCAGBEUF68PnfXYOoMQd7ziiAVXX4JR2UVG7RJuNbuFhk2Vrrloo1QEGIzgwyBzbJr0M7JlKTc6DgQbOmyUp_3jJljygbHULFGghkgeEzDhBJiTio8cYauZhW71HPeZMRqXEbdpKDIXjqcm7cpunEOypy-4HH6pTFsqlWr6dhw69w"

class SecretsTestCases(TestCase):
    def setUp(self):
        if not os.path.exists(TMP_PATH):
            os.makedirs(TMP_PATH)

    def tearDown(self):
        for f in glob.glob(f'{TMP_PATH}/*'):
            os.remove(f)

    def test_write_read_secrets(self):
        SecretsManager.mode = 'yaml'
        secrets_file_path = f'{TMP_PATH}/secrets.yml.enc'
        message = "TEST MESSAGE"
        write_secrets(message, TEST_KEY, secrets_file_path)
        decrypted = read_secrets(secrets_file_path, TEST_KEY)
        self.assertEqual(decrypted, message)

    def test_read_valid_yaml(self):
        SecretsManager.mode = 'yaml'
        with open(f"{ROOT}/encrypted_secrets/test_fixtures/valid_yaml.yml", "r") as valid_yaml_file:
            encrypted_yaml_path = f"{ROOT}/test_tmp/valid_encrypted_secrets.yml"
            yaml = valid_yaml_file.read()
            write_secrets(yaml, TEST_KEY, encrypted_yaml_path)
            SecretsManager.load(encrypted_yaml_path, TEST_KEY)
            self.assertEqual(get_secret('key_1'), 'value1')

    def test_read_invalid_yaml(self):
        SecretsManager.mode = 'yaml'
        with open(f"{ROOT}/encrypted_secrets/test_fixtures/invalid_yaml.yml", "r") as invalid_yaml_file:
            encrypted_yaml_path = f"{ROOT}/test_tmp/valid_encrypted_secrets.yml"
            yaml = invalid_yaml_file.read()
            write_secrets(yaml, TEST_KEY, encrypted_yaml_path)
            with self.assertRaises(YAMLFormatException):
                SecretsManager.load(encrypted_yaml_path, TEST_KEY)

    def test_env_mode(self):
        SecretsManager.load(env_mode=True)

