import os
import tempfile
import re
import subprocess
import encrypted_secrets.conf as secrets_conf
from encrypted_secrets.crypto.aes import AESCipher

def detect_mode(**kwargs):
    pass

def parse_env_string(env_string):
    envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
    result = {}

    for line in env_string.splitlines():
        if not line.startswith('#'):
            match = envre.match(line)
            if match is not None:
                result[match.group(1)] = match.group(2)

    return result

def write_secrets(message, key=secrets_conf.ENCRYPTED_SECRETS_KEY, encrypted_secrets_path=secrets_conf.ENCRYPTED_SECRETS_PATH):
    with open(encrypted_secrets_path, 'w') as encrypted_secrets_file:
        cipher = AESCipher(message, key)
        encrypted = cipher.encrypt()
        encrypted_secrets_file.write(encrypted)

def read_secrets(encrypted_secrets_file_path=secrets_conf.ENCRYPTED_SECRETS_PATH, key=secrets_conf.ENCRYPTED_SECRETS_KEY):
    key_file_exists = os.path.isfile(encrypted_secrets_file_path)

    # To handle first-run of init_secrets command when key is not yet set:
    if key is None or not key_file_exists:
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


