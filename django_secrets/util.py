import os
import tempfile
import subprocess
import django_secrets.conf as secrets_conf
from django_secrets.crypto.aes import AESCipher

def write_secrets(message, key=secrets_conf.ENCRYPTED_SECRETS_KEY):
    with open(secrets_conf.ENCRYPTED_SECRETS_PATH, 'w') as encrypted_secrets_file:
        cipher = AESCipher(message, key)
        encrypted = cipher.encrypt()
        encrypted_secrets_file.write(encrypted)

def read_secrets(encrypted_secrets_file_path=secrets_conf.ENCRYPTED_SECRETS_PATH, key=secrets_conf.ENCRYPTED_SECRETS_KEY):
    key_file_exists = os.path.isfile(encrypted_secrets_file_path)

    if not key_file_exists:
        return False

    with open(encrypted_secrets_file_path, 'r') as encrypted_secrets_file:
        message = encrypted_secrets_file.read()
        cipher = AESCipher(message, key)
        decrypted = cipher.decrypt()

    return decrypted

def check_editor():
    if not os.environ.get('EDITOR'):
        raise Exception('Unable to open editor; please set your EDITOR '
                        'environment variable to point to your preferred '
                        'editor, e.g. "/usr/bin/vim" or simply "vim"')
    return os.environ['EDITOR']

def edit_secrets():
    editor = check_editor()
    decrypted_content = read_secrets()
    fd, filename = tempfile.mkstemp(text=True)
    f = open(fd, 'w')
    f.write(decrypted_content)
    f.close()
    cmd = '%s %s' % (editor, filename)
    write_status = subprocess.call(cmd, shell=True)

    if write_status != 0:
        os.remove(filename)
        raise Exception("The editor returned a non-zero status "
                        "(that means it failed.)")
    f = open(filename)
    unencrypted_contents = f.read()
    write_secrets(unencrypted_contents)
    f.close()
    os.remove(filename)


