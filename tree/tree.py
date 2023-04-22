# Angel Higueros - 20460
# Laboratorio C

class Node:
    def init(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El valor debe ser una cadena de texto")
        
        self.valor = valor
        self.left = None
        self.right = None

def get_tree(postfix_expr):
    if not isinstance(postfix_expr, list):
        raise ValueError("La expresión debe ser una lista")

    stack = []
    operadores = {'+', '-', '*', '/'}

    for token in postfix_expr:
        if token not in operadores:
            nodo = Node(token)
        else:
            try:
                operando_derecho = stack.pop()
                operando_izquierdo = stack.pop()
            except IndexError as e:
                raise ValueError("La expresión es inválida") from e

            nodo = Node(token)
            nodo.left = operando_izquierdo
            nodo.right = operando_derecho
        stack.append(nodo)

    if len(stack) != 1:
        raise ValueError("La expresión es inválida")

    return stack.pop()

