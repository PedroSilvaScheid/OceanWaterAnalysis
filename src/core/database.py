import sqlite3
from datetime import datetime
from utils.paths import get_database_path
from config.config import MAX_HISTORY_ITEMS
class DatabaseManager:
    """
    Gerencia as operações de banco de dados para a aplicação
    Implementa o padrão Singleton para garantir uma única conexão com o banco
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa a conexão com o banco de dados e cria as tabelas necessárias"""
        self.db_path = get_database_path()
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
    
    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            local TEXT,
            ph REAL,
            salinidade REAL,
            temperatura REAL,
            indice_carbono REAL,
            data_hora TEXT
        )
        ''')
        self.conn.commit()
    
    def insert_analysis(self, local, ph, salinidade, temperatura, indice_carbono):
        """
        Insere uma nova análise no banco de dados
        
        Args:
            local (str): Local da coleta
            ph (float): Valor de pH
            salinidade (float): Valor de salinidade
            temperatura (float): Valor de temperatura
            indice_carbono (float): Valor do índice de carbono calculado
            
        Returns:
            str: Data e hora da inserção formatada
        """
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO analises (local, ph, salinidade, temperatura, indice_carbono, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (local, ph, salinidade, temperatura, indice_carbono, data_hora))
        self.conn.commit()
        
        return data_hora
    
    def get_recent_analyses(self, limit=MAX_HISTORY_ITEMS):
        """
        Obtém as análises mais recentes
        
        Args:
            limit (int, optional): Número máximo de registros a retornar. Padrão é 10.
            
        Returns:
            list: Lista de tuplas com os dados das análises
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT local, ph, salinidade, temperatura, indice_carbono, data_hora
            FROM analises ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def clear_history(self):
        """
        Remove todos os registros de análises do banco de dados
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM analises')
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()