class InputValidator:
    """
    Utilitário para validar entradas de usuário
    """
    @staticmethod
    def validate_float_input(value: str, field_name: str) -> tuple[bool, float, str]:
        """
        Valida um valor de entrada como número de ponto flutuante
        
        Args:
            value (str): O valor a ser validado
            field_name (str): Nome do campo para mensagem de erro
            
        Returns:
            tuple: (é_válido, valor_convertido, mensagem_de_erro)
        """
        if not value.strip():
            return False, 0.0, f"O campo {field_name} deve ser preenchido."
        
        try:
            float_value = float(value)
            return True, float_value, ""
        except ValueError:
            return False, 0.0, f"O valor de {field_name} deve ser um número válido."