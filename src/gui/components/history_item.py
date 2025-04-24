from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from gui.styles import AppStyles

class HistoryItem(QFrame):
    """
    Item individual para o histórico de análises
    """
    def __init__(self, local, ph, salinidade, temperatura, indice, data_hora, parent=None):
        super().__init__(parent)
        self.setFixedHeight(65)  # Altura fixa para todos os itens
        self.setStyleSheet(AppStyles.HISTORY_ITEM)
        # Formatar os valores com 2 casas decimais
        self.ph_formatado = f"{ph:.2f}"
        self.salinidade_formatada = f"{salinidade:.2f}"
        self.temperatura_formatada = f"{temperatura:.2f}"
        self.indice_formatado = f"{indice:.2f}"
        self.local = local
        self.data_hora = data_hora

        self._init_ui()
    
    def _init_ui(self):
        
        """Inicializa a interface do usuário"""
        # Layout de uma única linha para o item
        item_layout = QHBoxLayout(self)
        item_layout.setContentsMargins(10, 5, 10, 5)
        
        # Local (à esquerda)
        local_label = QLabel(f"<b>{self.local}</b>")
        local_label.setMinimumWidth(150)
        local_label.setMaximumWidth(250)
        item_layout.addWidget(local_label, 3)
        
        # Data/Hora
        data_label = QLabel(f"{self.data_hora}")
        data_label.setAlignment(Qt.AlignCenter)
        item_layout.addWidget(data_label, 2)
        
        # Valores (pH, salinidade, temperatura)
        ph_label = QLabel(f"pH: {self.ph_formatado}")
        salinidade_label = QLabel(f"Sal: {self.salinidade_formatada}")
        temperatura_label = QLabel(f"Temp: {self.temperatura_formatada}°C")
        
        item_layout.addWidget(ph_label, 1)
        item_layout.addWidget(salinidade_label, 1)
        item_layout.addWidget(temperatura_label, 1)
        
        # Valor do índice (em destaque à direita)
        indice_label = QLabel(f"<b>{self.indice_formatado}</b>")
        indice_label.setFont(QFont("Arial", 14, QFont.Bold))
        indice_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        indice_label.setMinimumWidth(60)
        
        item_layout.addWidget(indice_label, 1)