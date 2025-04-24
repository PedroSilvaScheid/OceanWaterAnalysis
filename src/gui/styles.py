class AppStyles:
    """
    Estilos centralizados para toda a aplicação
    """
    # Estilos gerais
    MAIN_WINDOW = """
        QMainWindow {
            background-color: #e6e9ed;
        }
        QLabel {
            color: #2c3e50;
        }
    """
    
    # Estilos para frames
    INPUT_FRAME = """
        #inputFrame {
            background-color: #f5f7fa;
            border-radius: 15px;
            padding: 15px;
        }
    """
    
    HIGHLIGHT_CARD = """
        #cardDestaque {
            background-color: #ecf0f1;
            border-radius: 15px;
            min-height: 180px;
        }
    """
    
    HISTORY_FRAME = """
        #historicoFrame {
            background-color: #f5f7fa;
            border-radius: 15px;
            padding: 15px;
        }
    """
    
    HISTORY_SCROLL = """
        QScrollArea {
            border: none;
            background-color: transparent;
        }
    """
    
    # Estilos para componentes
    LINE_EDIT = """
        QLineEdit {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px;
            background: white;
        }
    """
    
    CALCULATE_BUTTON = """
        QPushButton {
            background-color: #2e86de;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #1c71c7;
        }
        QPushButton:pressed {
            background-color: #0f5baa;
        }
    """
    
    CLEAR_BUTTON = """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
        QPushButton:pressed {
            background-color: #a93226;
        }
    """
    
    HISTORY_ITEM = """
        QFrame {
            background-color: white;
            border-radius: 10px;
            padding: 8px;
        }
        QFrame:hover {
            background-color: #f0f0f0;
        }
    """