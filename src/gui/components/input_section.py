from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from gui.styles import AppStyles

class InputSection(QFrame):
    """
    Componente para entrada de dados da análise de água
    """
    # Sinais
    calculate_requested = pyqtSignal(str, str, str, str)  # local, ph, sal, temp
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inputFrame")
        self.setStyleSheet(AppStyles.INPUT_FRAME)
        self.setMaximumHeight(170)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa a interface do usuário"""
        input_layout = QVBoxLayout(self)
        input_layout.setSpacing(10)
        
        # Título da seção
        titulo_input = QLabel("Dados da Amostra")
        titulo_input.setFont(QFont("Arial", 14, QFont.Bold))
        input_layout.addWidget(titulo_input)
        
        # Layout para os campos de entrada em uma única linha
        campos_layout = QHBoxLayout()
        campos_layout.setSpacing(15)
        
        # Campo Local
        self.local_input = self._create_input_field(
            campos_layout, "Local da Coleta:", 
            "Ex: Oceano Pacífico - Ponto 3", proportion=3
        )
        
        # Campo pH
        self.ph_input = self._create_input_field(
            campos_layout, "pH:", "Ex: 7.20"
        )
        
        # Campo Salinidade
        self.salinidade_input = self._create_input_field(
            campos_layout, "Salinidade:", "Ex: 33.56"
        )
        
        # Campo Temperatura
        self.temperatura_input = self._create_input_field(
            campos_layout, "Temperatura (°C):", "Ex: 25.30"
        )
        
        # Botão Calcular
        self._add_calculate_button(campos_layout)
        
        input_layout.addLayout(campos_layout)
    
    def _create_input_field(self, parent_layout, label_text, placeholder, proportion=1):
        """
        Cria um campo de entrada com label
        
        Args:
            parent_layout: Layout onde o campo será adicionado
            label_text (str): Texto do label
            placeholder (str): Texto placeholder do campo
            proportion (int): Proporção do campo no layout
            
        Returns:
            QLineEdit: O campo de entrada criado
        """
        field_layout = QVBoxLayout()
        field_layout.addWidget(QLabel(label_text))
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(AppStyles.LINE_EDIT)
        field_layout.addWidget(input_field)
        
        parent_layout.addLayout(field_layout, proportion)
        return input_field
    
    def _add_calculate_button(self, parent_layout):
        """Adiciona o botão de cálculo ao layout"""
        botao_layout = QVBoxLayout()
        botao_layout.addWidget(QLabel(""))  # Espaço para alinhamento
        
        self.calcular_btn = QPushButton("Calcular")
        self.calcular_btn.setFixedHeight(38)
        self.calcular_btn.setStyleSheet(AppStyles.CALCULATE_BUTTON)
        self.calcular_btn.clicked.connect(self._on_calculate)
        
        botao_layout.addWidget(self.calcular_btn)
        parent_layout.addLayout(botao_layout, 1)
    
    def _on_calculate(self):
        """Método chamado quando o botão Calcular é clicado"""
        local = self.local_input.text()
        ph = self.ph_input.text()
        salinidade = self.salinidade_input.text()
        temperatura = self.temperatura_input.text()
        
        self.calculate_requested.emit(local, ph, salinidade, temperatura)
    
    def clear_inputs(self):
        """Limpa todos os campos de entrada"""
        self.local_input.clear()
        self.ph_input.clear()
        self.salinidade_input.clear()
        self.temperatura_input.clear()