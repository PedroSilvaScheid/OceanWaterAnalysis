from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QScrollArea, QWidget, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt 

from gui.components.history_item import HistoryItem
from gui.styles import AppStyles


class HistorySection(QFrame):
    def __init__(self, db_manager, on_history_cleared, parent=None):
        super().__init__(parent)

        self.db_manager = db_manager
        self.on_history_cleared = on_history_cleared
        self.setObjectName("historicoFrame")
        self._init_ui()
    
    def _init_ui(self):
        self.setStyleSheet(AppStyles.HISTORY_FRAME)
    
        layout = QVBoxLayout(self)
        
        # Cabeçalho do histórico com título e botão limpar
        cabecalho_historico = QHBoxLayout()
        
        # Título da seção de histórico
        titulo_historico = QLabel("Histórico de Análises")
        titulo_historico.setFont(QFont("Arial", 14, QFont.Bold))
        cabecalho_historico.addWidget(titulo_historico)
        cabecalho_historico.addStretch()
        
        # Botão para limpar histórico
        self.limpar_btn = QPushButton("Limpar Histórico")
        self.limpar_btn.setStyleSheet(AppStyles.CLEAR_BUTTON)
        self.limpar_btn.clicked.connect(self.clear_history)
        cabecalho_historico.addWidget(self.limpar_btn)
        
        layout.addLayout(cabecalho_historico)
        
        # Container para as entradas do histórico
        self.historico_container = QWidget()
        self.historico_scroll = QScrollArea()
        self.historico_scroll.setWidgetResizable(True)
        self.historico_scroll.setWidget(self.historico_container)
        self.historico_scroll.setStyleSheet(AppStyles.HISTORY_SCROLL)
        
        self.historico_layout = QVBoxLayout(self.historico_container)
        self.historico_layout.setSpacing(10)
        
        layout.addWidget(self.historico_scroll)
    
    def clear_history(self):
        # Perguntar ao usuário para confirmar a ação
        confirmacao = QMessageBox()
        confirmacao.setIcon(QMessageBox.Warning)
        confirmacao.setWindowTitle("Confirmar Exclusão")
        confirmacao.setText("Tem certeza que deseja limpar todo o histórico?")
        confirmacao.setInformativeText("Esta ação não pode ser desfeita.")
        confirmacao.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmacao.setDefaultButton(QMessageBox.No)
        
        resposta = confirmacao.exec_()
        
        if resposta == QMessageBox.Yes:
            # Excluir todos os registros do banco de dados
            self.db_manager.clear_history()
            
            # Atualizar interface
            self.load_registers()
            
            # Notificar que o histórico foi limpo
            self.on_history_cleared()
            # Mostrar mensagem de sucesso
            QMessageBox.information(None, "Histórico Limpo", "O histórico foi limpo com sucesso.")
    
    def load_registers(self):
        # Limpar layout atual
        for i in reversed(range(self.historico_layout.count())):
            widget = self.historico_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Buscar os últimos 10 registros
        resultados = self.db_manager.get_recent_analyses()
        
        if resultados:
            # Adicionar todos os registros ao histórico
            for registro in resultados:
                item = HistoryItem(*registro)
                self.historico_layout.addWidget(item)
        else:
            # Sem registros
            sem_registros = QLabel("Nenhum registro encontrado.")
            sem_registros.setAlignment(Qt.AlignCenter)
            sem_registros.setFixedHeight(50)  # Manter consistência de altura
            self.historico_layout.addWidget(sem_registros)