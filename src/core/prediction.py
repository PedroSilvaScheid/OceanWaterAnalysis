import os
import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor

from utils.paths import get_model_path, get_scaler_path, get_mse_path, get_csv_path, get_model_dir

class PredictionModel:
    """
    Classe responsável por treinar, carregar e utilizar o modelo de predição
    Implementa o padrão Singleton para garantir uma única instância do modelo carregado
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionModel, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        """Inicializa o modelo - carregando ou treinando conforme necessário"""
        os.makedirs(get_model_dir(), exist_ok=True)
        
        model_path = get_model_path()
        scaler_path = get_scaler_path()
        mse_path = get_mse_path()
        
        # Verificar se o modelo, o scaler e o mse já foram salvos
        if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(mse_path):
            self._load_existing_model(model_path, scaler_path, mse_path)
        else:
            self._train_new_model(model_path, scaler_path, mse_path)
    
    def _load_existing_model(self, model_path, scaler_path, mse_path):
        """Carrega um modelo existente dos arquivos salvos"""
        self._rf_model = joblib.load(model_path)
        self._scaler = joblib.load(scaler_path)
        with open(mse_path, 'r') as mse_file:
            mse_data = json.load(mse_file)
            self._mse = mse_data['mse']
    
    def _train_new_model(self, model_path, scaler_path, mse_path):
        """Treina um novo modelo a partir dos dados brutos"""
        # Carregar e preparar dados
        data = self._load_and_prepare_data()
        
        X = data[['ph', 'sal', 'temp']]
        y = data['dic']

        # Dividir os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Normalizar os dados
        self._scaler = StandardScaler()
        X_train_scaled = self._scaler.fit_transform(X_train)
        X_test_scaled = self._scaler.transform(X_test)

        # Treinar modelo de Random Forest
        self._rf_model = RandomForestRegressor(n_estimators=150, random_state=42)
        self._rf_model.fit(X_train_scaled, y_train)

        # Salvar modelo e scaler
        self._save_model_artifacts(model_path, scaler_path)
        
        # Avaliar o modelo
        self._evaluate_and_save_metrics(X_test_scaled, y_test, mse_path)
    
    def _load_and_prepare_data(self):
        """Carrega e prepara os dados para treinamento"""
        csv_path = get_csv_path()
        enc_path = csv_path + '.enc'
        if os.path.exists(enc_path):
            from utils.crypto import load_key_from_env, decrypt_bytes
            key = load_key_from_env()
            if not key:
                raise RuntimeError('Encrypted CSV found but CSV_ENC_KEY not set in environment')
            with open(enc_path, 'rb') as f:
                enc_bytes = f.read()
            plain = decrypt_bytes(enc_bytes, key)
            from io import BytesIO
            data = pd.read_csv(BytesIO(plain), delimiter=';')
        else:
            data = pd.read_csv(csv_path, delimiter=';')
        
        # Limpar e converter dados
        data.columns = data.columns.str.strip()
        data['ph'] = data['ph'].astype(float)
        data['sal'] = data['sal'].astype(float)
        data['temp'] = data['temp'].astype(float)
        data['dic'] = data['dic'].astype(float)
        
        return data
    
    def _save_model_artifacts(self, model_path, scaler_path):
        """Salva o modelo e o scaler em arquivos"""
        joblib.dump(self._rf_model, model_path)
        joblib.dump(self._scaler, scaler_path)
    
    def _evaluate_and_save_metrics(self, X_test_scaled, y_test, mse_path):
        """Avalia o modelo e salva as métricas"""
        # Prever os valores no conjunto de teste
        y_pred_rf = self._rf_model.predict(X_test_scaled)

        # Calcular o MSE para o modelo treinado
        self._mse = mean_squared_error(y_test, y_pred_rf)

        # Salvar o MSE em um arquivo JSON
        mse_data = {'mse': self._mse}
        with open(mse_path, 'w') as mse_file:
            json.dump(mse_data, mse_file)

        # Calcular e exibir o R²
        r2_rf = r2_score(y_test, y_pred_rf)
        print(f"R² (Random Forest): {r2_rf}")
        print(f"MSE: {self._mse}")
    
    def predict_dic(self, ph, sal, temp):
        """
        Faz uma predição do índice de carbono com base nos parâmetros fornecidos
        
        Args:
            ph (float): O valor de pH da amostra
            sal (float): O valor de salinidade da amostra
            temp (float): O valor de temperatura da amostra
            
        Returns:
            float: O valor previsto do índice de carbono (DIC)
        """
        dados_usuario = pd.DataFrame([[ph, sal, temp]], columns=['ph', 'sal', 'temp'])
        dados_usuario_scaled = self._scaler.transform(dados_usuario)
        dic_previsto = self._rf_model.predict(dados_usuario_scaled)
        return dic_previsto[0]