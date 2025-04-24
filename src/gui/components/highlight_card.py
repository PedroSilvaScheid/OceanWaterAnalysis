from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from gui.styles import AppStyles

class HighlightCard(QFrame):
    """
    Card de destaque para mostrar a análise mais recente
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cardDestaque")
        self.setStyleSheet(AppStyles.HIGHLIGHT_CARD)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa a interface do usuário"""
        self.card_layout = QVBoxLayout(self)
        
        # Cabeçalho do card
        cabecalho_layout = QHBoxLayout()
        
        self.card_local = QLabel("Sem análises recentes")
        self.card_local.setFont(QFont("Arial", 11))
        cabecalho_layout.addWidget(self.card_local)
        
        cabecalho_layout.addStretch()
        
        self.card_data = QLabel("")
        self.card_data.setFont(QFont("Arial", 11))
        cabecalho_layout.addWidget(self.card_data)
        self.card_layout.addLayout(cabecalho_layout)
        
        # Legenda "Índice de Carbono"
        self.card_legenda = QLabel("Índice de Carbono")
        self.card_legenda.setAlignment(Qt.AlignCenter)
        self.card_legenda.setFont(QFont("Arial", 14))
        self.card_layout.addWidget(self.card_legenda)
        
        # Valor central
        self.card_valor = QLabel("--")
        self.card_valor.setAlignment(Qt.AlignCenter)
        self.card_valor.setFont(QFont("Arial", 36, QFont.Bold))
        self.card_layout.addWidget(self.card_valor)
        
        # Valores de entrada
        valores_layout = QHBoxLayout()
        valores_layout.setAlignment(Qt.AlignCenter)
        
        self.card_ph = QLabel("pH: --")
        self.card_salinidade = QLabel("Salinidade: --")
        self.card_temperatura = QLabel("Temperatura: --")
        
        for label in [self.card_ph, self.card_salinidade, self.card_temperatura]:
            label.setFont(QFont("Arial", 11))
            valores_layout.addWidget(label)
            valores_layout.addSpacing(20)
        
        self.card_layout.addLayout(valores_layout)
    
    def update_card(self, local="", ph=0, salinidade=0, temperatura=0, indice=0, data_hora=""):
        """
        Atualiza o card com os dados de uma análise
        
        Args:
            local (str): Local da coleta
            ph (float): Valor de pH
            salinidade (float): Valor de salinidade
            temperatura (float): Valor de temperatura
            indice (float): Valor do índice de carbono
            data_hora (str): Data e hora da análise
        """
        if not local:
            self.reset()
            return
            
        # Formatar os valores com as casas decimais apropriadas
        ph_formatado = f"{ph:.2f}"
        salinidade_formatada = f"{salinidade:.2f}"
        temperatura_formatada = f"{temperatura:.2f}"
        indice_formatado = f"{indice:.3f}"  # 3 casas decimais para o índice
        
        self.card_local.setText(local)
        self.card_data.setText(data_hora)
        self.card_valor.setText(indice_formatado)
        self.card_ph.setText(f"pH: {ph_formatado}")
        self.card_salinidade.setText(f"Salinidade: {salinidade_formatada}")
        self.card_temperatura.setText(f"Temperatura: {temperatura_formatada}°C")
    
    def reset(self):
        """Reset do card para o estado inicial"""
        self.card_local.setText("Sem análises recentes")
        self.card_data.setText("")
        self.card_valor.setText("--")
        self.card_ph.setText("pH: --")
        self.card_salinidade.setText("Salinidade: --")
        self.card_temperatura.setText("Temperatura: --")