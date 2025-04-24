from core.models import WaterAnalysis
from core.prediction import PredictionModel
from utils.validators import InputValidator

class AnalysisController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.predictor = PredictionModel()

    def process_analysis(self, local, ph_input, salinidade_input, temperatura_input):
        erros = []

        if not local.strip():
            erros.append("O local da coleta deve ser preenchido.")

        ph_ok, ph, erro = InputValidator.validate_float_input(ph_input, "pH")
        if not ph_ok: erros.append(erro)

        sal_ok, salinidade, erro = InputValidator.validate_float_input(salinidade_input, "Salinidade")
        if not sal_ok: erros.append(erro)

        temp_ok, temperatura, erro = InputValidator.validate_float_input(temperatura_input, "Temperatura")
        if not temp_ok: erros.append(erro)

        if erros:
            return False, erros

        indice_carbono = self.predictor.predict_dic(ph, salinidade, temperatura)
        analise = WaterAnalysis(local, ph, salinidade, temperatura, indice_carbono)

        valido, erro_validacao = analise.validate()
        if not valido:
            return False, [erro_validacao]

        self.db_manager.insert_analysis(
            analise.local, analise.ph, analise.salinidade, analise.temperatura, analise.indice_carbono
        )

        return True, analise

