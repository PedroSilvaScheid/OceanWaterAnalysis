import os
from cryptography.fernet import Fernet
import sys

try:
    import winreg
except Exception:
    winreg = None


def load_key_from_env(env_var='CSV_ENC_KEY'):
    """Load base64 key from environment variable."""
    key = os.environ.get(env_var)
    if not key:
        # fallback: when running as an installed app, the installer can write the key
        # to the Windows registry under HKLM\Software\<AppName>\CSV_ENC_KEY or HKCU.
        if winreg and getattr(sys, 'frozen', False):
            try:
                # First try HKLM (requires admin), then HKCU
                app_name = os.path.splitext(os.path.basename(sys.executable))[0]
                reg_path = r"Software\\%s" % app_name
                for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
                    try:
                        with winreg.OpenKey(hive, reg_path, 0, winreg.KEY_READ) as key_handle:
                            val, _ = winreg.QueryValueEx(key_handle, 'CSV_ENC_KEY')
                            if val:
                                return val.encode()
                    except OSError:
                        continue
            except Exception:
                return None
        return None
    return key.encode()


def decrypt_bytes(enc_bytes, key):
    f = Fernet(key)
    return f.decrypt(enc_bytes)


def encrypt_file(in_path, out_path, key):
    f = Fernet(key)
    with open(in_path, 'rb') as fin:
        data = fin.read()
    token = f.encrypt(data)
    with open(out_path, 'wb') as fout:
        fout.write(token)


def generate_key():
    return Fernet.generate_key()
