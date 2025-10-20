import os
import sys
from config.config import DB_FILENAME, MODEL_FILENAME, SCALER_FILENAME, MSE_FILENAME, CSV_FILENAME


def get_resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funcionando em ambiente de desenvolvimento
    e em executável PyInstaller.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, relative_path)


def _get_user_data_dir():
    """
    Return a writable per-user data directory. When running as a frozen executable
    we should store runtime-writable artifacts (database, trained model) in
    %LOCALAPPDATA%\<AppName> (or APPDATA fallback). During development, keep
    files under the project layout.
    """
    # If running frozen (PyInstaller) prefer LocalAppData
    if getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS'):
        app_name = os.path.splitext(os.path.basename(sys.executable))[0]
        local_appdata = os.environ.get('LOCALAPPDATA') or os.environ.get('APPDATA') or os.path.expanduser('~')
        data_dir = os.path.join(local_appdata, app_name)
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    # Development: use project structure
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_model_dir():
    # Save model artifacts in the user data dir when frozen so they are writable
    if getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS'):
        return os.path.join(_get_user_data_dir(), 'model')
    return get_resource_path(os.path.join('src', 'model'))


def get_utils_dir():
    return get_resource_path(os.path.join('src', 'utils'))


def get_database_path():
    # For packaged apps use a writable user-local path, otherwise use project-level path
    if getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS'):
        return os.path.join(_get_user_data_dir(), DB_FILENAME)
    return get_resource_path(DB_FILENAME)


def get_csv_path():
    return os.path.join(get_utils_dir(), CSV_FILENAME)


def get_model_path():
    return os.path.join(get_model_dir(), MODEL_FILENAME)


def get_scaler_path():
    return os.path.join(get_model_dir(), SCALER_FILENAME)


def get_mse_path():
    return os.path.join(get_model_dir(), MSE_FILENAME)
