import re

def deteccion2(regex):
    if regex.count('[') != regex.count(']'):
        print("[Error]: Corchetes inconsistentes.")
        return False, regex

    if regex.count('(') != regex.count(')'):
        print("[Error]: Paréntesis inconsistentes.")
        return False, regex

    if not re.match(r"[a-zA-Z0-9ε]*", regex):
        print("[Error]: No  se encontraron letras o números en r")
        return False, regex

    if re.match(r"^[*+]", regex):
        print("[Error]: No es posible inciar r con los siguientes simbolos [ *,   +. ] ")
        return False, regex

    if re.search(r"\|$", regex):
        print("[Error]: No es posible terminar r con los siguientes simbolos [  |. ]")
        return False, regex

    return True, regex
