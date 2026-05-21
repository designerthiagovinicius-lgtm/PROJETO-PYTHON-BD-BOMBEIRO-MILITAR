#comentario: Este código é um módulo de validação que contém várias funções para validar diferentes tipos de dados, 
# como nomes, emails, telefones, placas de veículos, IDs numéricos, quantidades, datas e PINs. Essas funções são usadas 
# em outros serviços do sistema para garantir que os dados inseridos pelos usuários sejam corretos e seguros antes de 
# serem processados ou armazenados no banco de dados. Cada função retorna um valor booleano indicando se a validação foi 
# bem-sucedida ou não, e imprime mensagens de erro específicas quando a validação falha. Essas validações são essenciais 
# para manter a integridade dos dados e evitar erros ou vulnerabilidades no sistema de gestão militar.    

def validar_nome(nome: str, min_chars: int = 3, max_chars: int = 100) -> bool:
    """
    Valida se o nome tem o mínimo e máximo de caracteres e não está vazio.
    
    Parâmetros:
    - nome: string a validar
    - min_chars: número mínimo de caracteres (padrão: 3)
    - max_chars: número máximo de caracteres (padrão: 100)
    
    Retorna:
    - True se válido, False caso contrário
    """
    if not nome or len(nome.strip()) < min_chars:
        print(f"Erro: O nome deve ter pelo menos {min_chars} caracteres e não pode estar vazio.")
        return False
    
    if len(nome.strip()) > max_chars:
        print(f"Erro: O nome não pode ter mais de {max_chars} caracteres.")
        return False
    
    return True


def validar_email(email: str) -> bool:
    """
    Valida se o email não está vazio e contém um '@'.
    
    Parâmetros:
    - email: string a validar
    
    Retorna:
    - True se válido, False caso contrário
    """
    if not email or len(email.strip()) == 0:
        print("Erro: O email não pode estar vazio.")
        return False
    
    if '@' not in email:
        print("Erro: O email deve conter um '@'.")
        return False
    
    return True


def validar_telefone(telefone: str, min_digitos: int = 8, max_digitos: int = 15) -> bool:
    """
    Valida se o telefone contém apenas números e tem entre min_digitos e max_digitos dígitos.
    
    Parâmetros:
    - telefone: string a validar
    - min_digitos: número mínimo de dígitos (padrão: 8)
    - max_digitos: número máximo de dígitos (padrão: 15)
    
    Retorna:
    - True se válido ou vazio, False caso contrário
    """
    if not telefone:
        return True  # Telefone pode ser vazio
    
    telefone_limpo = ''.join(filter(str.isdigit, telefone))
    
    if len(telefone_limpo) < min_digitos or len(telefone_limpo) > max_digitos:
        print(f"Erro: O telefone deve ter entre {min_digitos} e {max_digitos} dígitos.")
        return False
    
    return True


def validar_placa(placa: str, min_chars: int = 6, max_chars: int = 10) -> bool:
    """
    Valida se a placa não está vazia e tem entre min_chars e max_chars caracteres.
    
    Parâmetros:
    - placa: string a validar
    - min_chars: número mínimo de caracteres (padrão: 6)
    - max_chars: número máximo de caracteres (padrão: 10)
    
    Retorna:
    - True se válido, False caso contrário
    """
    if not placa or len(placa.strip()) == 0:
        print("Erro: A placa não pode estar vazia.")
        return False
    
    if len(placa.strip()) < min_chars or len(placa.strip()) > max_chars:
        print(f"Erro: A placa deve ter entre {min_chars} e {max_chars} caracteres.")
        return False
    
    return True


def validar_id_numerico(valor, nome_campo: str = "ID") -> int:
    """
    Valida se um valor é um ID numérico válido.
    
    Parâmetros:
    - valor: valor a validar
    - nome_campo: nome do campo para mensagem de erro
    
    Retorna:
    - ID convertido para int se válido, None caso contrário
    """
    try:
        return int(valor)
    except (ValueError, TypeError):
        print(f"Erro: O {nome_campo} deve ser um número inteiro.")
        return None


def validar_quantidade(quantidade, min_valor: int = 0, max_valor: int = 999999) -> int:
    """
    Valida se a quantidade é um número inteiro dentro de um intervalo.
    
    Parâmetros:
    - quantidade: valor a validar
    - min_valor: valor mínimo (padrão: 0)
    - max_valor: valor máximo (padrão: 999999)
    
    Retorna:
    - Quantidade convertida para int se válida, None caso contrário
    """
    try:
        qtd = int(quantidade)
        
        if qtd < min_valor:
            print(f"Erro: A quantidade não pode ser menor que {min_valor}.")
            return None
        
        if qtd > max_valor:
            print(f"Erro: A quantidade não pode ser maior que {max_valor}.")
            return None
        
        return qtd
    except (ValueError, TypeError):
        print("Erro: A quantidade deve ser um número inteiro.")
        return None


def validar_data(data_str: str, formato: str = '%Y-%m-%d') -> bool:
    """
    Valida se a data está em um formato válido.
    
    Parâmetros:
    - data_str: string a validar
    - formato: formato esperado da data (padrão: '%Y-%m-%d')
    
    Retorna:
    - True se válida, False caso contrário
    """
    from datetime import datetime
    
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        print(f"Erro: A data deve estar no formato {formato} (ex: 2024-12-31).")
        return False


def validar_pin(pin: str) -> bool:
    """
    Valida se o PIN é uma sequência de 4 dígitos.
    
    Parâmetros:
    - pin: string a validar
    
    Retorna:
    - True se válido, False caso contrário
    """
    if not pin or not pin.isdigit() or len(pin) != 4:
        print("Erro: O PIN deve conter exatamente 4 números.")
        return False
    
    return True


def validar_comprimento_texto(texto: str, min_chars: int = 1, max_chars: int = 255, nome_campo: str = "Campo") -> bool:
    """
    Valida se um texto está dentro de um intervalo de caracteres.
    
    Parâmetros:
    - texto: string a validar
    - min_chars: número mínimo de caracteres
    - max_chars: número máximo de caracteres
    - nome_campo: nome do campo para mensagem de erro
    
    Retorna:
    - True se válido, False caso contrário
    """
    if not texto:
        return True  # Campo pode ser vazio
    
    texto_limpo = texto.strip()
    
    if len(texto_limpo) < min_chars:
        print(f"Erro: {nome_campo} deve ter pelo menos {min_chars} caracteres.")
        return False
    
    if len(texto_limpo) > max_chars:
        print(f"Erro: {nome_campo} não pode ter mais de {max_chars} caracteres.")
        return False
    
    return True


def validar_campo_obrigatorio(valor, nome_campo: str = "Campo") -> bool:
    """
    Valida se um campo obrigatório está preenchido.
    
    Parâmetros:
    - valor: valor a validar
    - nome_campo: nome do campo para mensagem de erro
    
    Retorna:
    - True se preenchido, False caso contrário
    """
    if not valor or (isinstance(valor, str) and len(valor.strip()) == 0):
        print(f"Erro: {nome_campo} é obrigatório.")
        return False
    
    return True


def validar_opcao_lista(valor: str, opcoes_validas: list, nome_campo: str = "Opção") -> bool:
    """
    Valida se um valor está dentro de uma lista de opções válidas.
    
    Parâmetros:
    - valor: valor a validar
    - opcoes_validas: lista de opções válidas
    - nome_campo: nome do campo para mensagem de erro
    
    Retorna:
    - True se válido, False caso contrário
    """
    if valor not in opcoes_validas:
        print(f"Erro: {nome_campo} deve ser uma das seguintes opções: {', '.join(opcoes_validas)}")
        return False
    
    return True
# Validações adicionais podem ser adicionadas aqui conforme necessário para o sistema de gestão militar.