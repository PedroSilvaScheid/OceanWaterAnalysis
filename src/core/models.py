from dataclasses import dataclass
from typing import Optional

@dataclass
class WaterAnalysis:
    """
    Modelo de dados para análise de água
    """
    local: str
    ph: float
    salinidade: float
    temperatura: float
    indice_carbono: float = 0.0
    data_hora: str = ""
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Valida os dados da análise
        
        Returns:
            tuple: (é_válido, mensagem_de_erro)
        """
        # Verificar se o campo local está preenchido
        if not self.local:
            return False, "O local da coleta deve ser preenchido."
        
        # Validações de faixa de valores
        if not (0 <= self.ph <= 14):
            return False, "O pH deve estar entre 0 e 14."
            
        if self.salinidade < 0:
            return False, "A Salinidade não pode ser negativa."
            
        if self.temperatura < -20 or self.temperatura > 50:
            return False, "A Temperatura deve estar entre -20°C e 50°C."
        
        return True, None