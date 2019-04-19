import os, glob
from django.test import TestCase
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.util import *

TMP_PATH = f'{os.getcwd()}/test_tmp'

class SecretsTestCases(TestCase):
    def setUp(self):
        if not os.path.exists(TMP_PATH):
            os.makedirs(TMP_PATH)

    def tearDown(self):
        for f in glob.glob(f'{TMP_PATH}/*'):
            os.remove(f)

    def test_write_read_secrets(self):
        secrets_conf.ENCRYPTED_SECRETS_PATH = f'{TMP_PATH}/secrets.yml.enc'
        message = "TEST MESSAGE"
        key = "TEST KEY"
        write_secrets(message, key)
        decrypted = read_secrets(secrets_conf.ENCRYPTED_SECRETS_PATH, key)
        self.assertEqual(decrypted, message)

