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
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_model_dir():
    return get_resource_path(os.path.join("src", "model"))

def get_utils_dir():
    return get_resource_path(os.path.join("src", "utils"))

def get_database_path():
    return get_resource_path(DB_FILENAME)

def get_csv_path():
    return os.path.join(get_utils_dir(), CSV_FILENAME)

def get_model_path():
    return os.path.join(get_model_dir(), MODEL_FILENAME)

def get_scaler_path():
    return os.path.join(get_model_dir(), SCALER_FILENAME)

def get_mse_path():
    return os.path.join(get_model_dir(), MSE_FILENAME)
