# Angel Higueros - 20460
# Laboratorio C

def validar_precedencia(simbolo: str) -> int:
    precedencias = {'|': 1, '.': 2, '*': 3}
    return precedencias.get(simbolo, 0)


def infix_postfix(infix_expr: str) -> str:
    try:
        # Definir los símbolos válidos y los operadores binarios
        simbolos = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789().+*?|'[]\-/_;:=<>\"")
        operadores = {"|"}

        # Crear una lista vacía para almacenar la expresión posfija y una stack vacía para el algoritmo
        expresion_posfija = []
        stack = []

        # Contador para verificar si el regex está balanceado
        contador_parentesis = 0

        for i in infix_expr:

            # Verificar si el carácter es válido
            if i not in simbolos:
                print(f"\n[!] El carácter '{i}' no es válido")
                exit()
            if i == '(':
                contador_parentesis += 1
                stack.append(i)
            elif i == ')':
                contador_parentesis -= 1
                while stack[-1] != "(":
                    expresion_posfija.append(stack.pop())
                stack.pop()
            elif i in operadores:
                while stack and stack[-1] != '(' and validar_precedencia(i) <= validar_precedencia(stack[-1]):
                    expresion_posfija.append(stack.pop())
                stack.append(i)
            else:
                if (
                    expresion_posfija
                    and expresion_posfija[-1] not in operadores
                ):
                    expresion_posfija.append('.')
                expresion_posfija.append(i)

        while stack:
            expresion_posfija.append(stack.pop())

        if contador_parentesis == 0:
            if resultado := ''.join(expresion_posfija):
                return resultado
            print('\n[!] La expresión posfija está vacía')
        else:
            print('\n[!] El regex no está balanceado')
        exit()
    except Exception:
        print('\n[!] El regex no es una expresion valida')
        exit()


