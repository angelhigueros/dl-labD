# Angel Higueros - 20460
# Laboratorio C

class Yalex:
    def __init__(self, especificaciones):
        self.especificaciones = especificaciones
        self.definiciones = {}
        self.comentarios = []
        self.funciones = []
        self.trailer = None
        self.funciones_en_progreso = False
        self.trailer_agregado = False
        self.regex = None

    def get_regex(self):
        self.parse_file()

        # Parseo de las expresiones de definiciones
        for expresion, valor in self.definiciones.items():
            if '-' not in valor:
                continue

            inicio, fin = valor.split('-')
            valores = [chr(caracter) for caracter in range(ord(inicio), ord(fin) + 1)]
            valores = '|'.join(valores)

            if len(valores) == 1:
                valores = valores[0]

            self.definiciones[expresion] = valores

    def parse_file(self):
        for linea in self.especificaciones:
            partes = linea.split()

            if not partes:
                if self.funciones_en_progreso and not self.trailer_agregado:
                    self.trailer_agregado = True
                continue

            if '(*' in partes and '*)' in partes:
                comentario = partes[partes.index('(*'):partes.index('*)')+1]

                if not self.comentarios:
                    self.comentarios.append(comentario)
                elif self.trailer_agregado and not self.funciones:
                    self.trailer = comentario
                else:
                    del partes[partes.index('(*'):partes.index('*)')+1]
                    self.comentarios.append(comentario)

                if not partes:
                    continue

            if partes[0] == 'let':
                variable, valor = partes[1], partes[-1]

                if valor.startswith('[') and valor.endswith(']') and '-' in valor:
                    self.definiciones[variable] = valor[1:-1]
                else:
                    self.definiciones[variable] = valor

            elif self.funciones_en_progreso:
                if '|' in partes:
                    self.funciones.append(partes[1:])
                else:
                    self.funciones.append(partes)

            elif partes[0] == 'rule':
                self.funciones.append(partes[1])
                self.funciones_en_progreso = True

    def parse_especificaciones(self):  # sourcery skip: low-code-quality
        for linea in self.especificaciones:
            partes = linea.split()
            if len(partes) < 1:
                if self.funciones_en_progreso and not self.trailer_agregado:
                    self.trailer_agregado = True
            else:
                # Comentarios
                if '(*' in partes and '*)' in partes:
                    comentario = partes[partes.index('(*'):partes.index('*)')+1]
                    if not self.comentarios:
                        self.comentarios.append(comentario)
                    elif self.trailer_agregado and not self.funciones:
                        self.trailer = comentario
                    else:
                        del partes[partes.index('(*'):partes.index('*)')+1]
                        self.comentarios.append(comentario)
                        if not partes:
                            continue

                if partes[0] == 'let':
                    valor = partes[-1]
                    if valor.startswith('[') and valor.endswith(']') and '-' in valor:
                        valores_ = valor[1:-1].split('-')
                        valores_resultantes = [chr(caracter) for caracter in range(ord(valores_[0]), ord(valores_[1])+1)]
                        valores_resultantes = '|'.join(valores_resultantes)
                        if len(valores_resultantes) == 1:
                            valores_resultantes = valores_resultantes[0]
                        self.definiciones[partes[1]] = valores_resultantes
                    else:
                        self.definiciones[partes[1]] = valor

