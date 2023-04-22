import re

# Clase para detectar errores.

def deteccion(regex):

    parent = check_parenthesis(regex)

    if not parent:
        print("[Error]: Paréntesis inconsistentes\n")
        return False

    coin = re.match(r"[a-zA-Z0-9ε]*", regex)

    if not coin:
        print("[Error]:No  se encontraron letras o números en r☻n")
        return False


    coincidencia = re.match(r"^(?![*+]).*", regex)

    if not coincidencia:
        print("[Error]: No es posible inciar r con los siguientes simbolos [ *,   +. ] ")
        return False
    
    coincidencia = re.match(r".*(?<!\|)$", regex)

    if not coincidencia:
        print("[Error]: No es posible terminar r con los siguientes simbolos [  | ]")
        return False

    if re.search("\-", regex):
        print("[!] Expresión regular válida")
        return True

    return True

def check_parenthesis(regex):
    stack = []
    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if len(stack) == 0:
                return False
            stack.pop()

    return len(stack) == 0