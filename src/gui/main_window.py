import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from core.database import DatabaseManager
from core.models import WaterAnalysis
from core.controllers.analysis_controller import AnalysisController

from gui.components.input_section import InputSection
from gui.components.highlight_card import HighlightCard
from gui.components.history_section import HistorySection
from gui.styles import AppStyles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análise de Água - Índice de Carbono")
        self.setMinimumSize(800, 700)
        
        # Inicializar gerenciador de banco de dados
        self.db_manager = DatabaseManager()

        # Inicializar controler
        self.controller = AnalysisController(self.db_manager)

        # Configurar interface
        self._init_ui()
        
        # Carregar registros existentes
        self.update_interface()
    
    def _init_ui(self):
        # Estilizar janela
        self.setStyleSheet(AppStyles.MAIN_WINDOW)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Seção de entrada de dados
        self.input_section = InputSection(self)
        self.input_section.calculate_requested.connect(self.exec_calculate) 
        main_layout.addWidget(self.input_section)

        # Card de destaque
        self.highlight_card = HighlightCard(self)
        main_layout.addWidget(self.highlight_card)
        
        # Seção de histórico
        self.history_section = HistorySection(self.db_manager, self.clean_highlight_card, self)
        main_layout.addWidget(self.history_section)
        
        # Ajustar proporções das seções
        main_layout.setStretch(0, 1)  # Input section
        main_layout.setStretch(1, 2)  # Card destaque
        main_layout.setStretch(2, 4)  # Histórico
   
    def exec_calculate(self, local, ph, salinidade, temperatura):
        sucesso, resultado = self.controller.process_analysis(local, ph, salinidade, temperatura)
        
        if not sucesso:
            self.show_error_dialog(resultado)
            return

        self.update_interface()
        self.input_section.clear_inputs()

    def show_error_dialog(self, mensagens):
        erro_dialog = QMessageBox(self)
        erro_dialog.setIcon(QMessageBox.Warning)
        erro_dialog.setWindowTitle("Erro de Validação")
        erro_dialog.setText("Não foi possível realizar o cálculo")
        erro_dialog.setInformativeText("\n".join(mensagens))
        erro_dialog.setStandardButtons(QMessageBox.Ok)
        erro_dialog.exec_()
    
    def update_interface(self):
        # Obter registros recentes
        registros = self.db_manager.get_recent_analyses(1)
        
        # Atualizar card de destaque
        if registros:
            self.highlight_card.update_card(*registros[0])
        
        # Atualizar seção de histórico
        self.history_section.load_registers()
    
    def clean_highlight_card(self):
        # Limpar o card de destaque
        self.highlight_card.reset()
    
    def closeEvent(self, event):
        # Fechar conexão com o banco de dados
        self.db_manager.close()
        super().closeEvent(event)