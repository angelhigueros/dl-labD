from otros.reg import evaluar
from tree.Thompson import *
from otros.Errores import *
from tools.AFD_Converter import *
from automatas.SintaxT import *
from otros.ErroresArchivo import *
import re
from otros.SimuladorTxT import *

def analizar(archivo, yalex):

    tabla = {} 
    res_list = [] 


    with open(yalex, "r", encoding='utf-8') as file:
        data = file.read()
        regex_let = r"let (\w+) = (.*)"
        variables = re.findall(regex_let, data)

        for var in variables: 
            bool, expres = deteccion2(var[1])

            if bool == "Corchetes": 
                print("\n[ERROR]")
                print("r: ", expres)
                print("Linea: ", data.count('\n', 0, data.find(expres)))
                print("Error: Corchetes inconsistentes\n")
                
            
            if bool == "Parent":
                print("\n[ERROR]")
                print("r: ", expres)
                print("Linea: ", data.count('\n', 0, data.find(expres)))
                print("Error: Paréntesis inconsistentes\n")
            
            if bool == "BB":
                print("\n[ERROR]")
                print("Linea: ", data.count('\n', 0, data.find(expres)) )
                print("Error: No es posible inciar r con los siguientes simbolos [ *,   +. ]\n")
            
            if bool == "OF":
                print("Linea: ", data.count('\n', 0, data.find(expres)))
                print("Error: No es posible terminar r con los siguientes simbolos [  |. ]")
            

            bool, expres = deteccion2(var[0])
            
            if bool == "Corchetes":
                print("\n[ERROR]")
                print("r: ", expres)
                print("Línea: ", data.count('\n', 0, data.find(expres)))
                print("Error: Corchetes inconsistentes")
            
            if bool == "Parent":
                print("\n[ERROR]")
                print("r: ", expres)
                print("Línea: ", data.count('\n', 0, data.find(expres)))
                print("Error: Paréntesis inconsistentes")
            
            if bool == False: 
                print("\n[ERROR]")
                print("Línea: ", data.count('\n', 0, data.find(expres)))
                print("Error: No  se encontraron letras o números en r")

            if bool == "BB":
                print("\n[ERROR]")
                print("Error en la línea: ", data.count('\n', 0, data.find(expres)))
                print("Error: No es posible inciar r con los siguientes simbolos [ *,   +. ]\n")

            if bool == "OF":
                print("\n[ERROR]")
                print("Línea: ", data.count('\n', 0, data.find(expres)))
                print("Error: No es posible terminar r con los siguientes simbolos [  |. ]")

        # Jalando los tokens especiales.
        if "rule gettoken =" in data:
            cadena_tokens = data[data.find("rule gettoken ="):]
            lista_tokens = cadena_tokens.split("|")
            diccionario_tokens = {}
            for token in lista_tokens:
                nombre, valor = token.split("return")
                diccionario_tokens[nombre.strip()] = valor.strip().strip("\"")

            nuevo_diccionario = {}
            for clave, valor in diccionario_tokens.items():
                clave_limpia = clave.replace('rule gettoken = \n', "").strip()
                nuevo_diccionario[clave_limpia] = valor

            diccionario_ordenado = dict(sorted(nuevo_diccionario.items()))

            lista_temp = []

            for clave in diccionario_ordenado.keys():
                palabra = clave.replace('{', '').strip()
                lista_temp.append(palabra)
            

            for elemento in lista_temp:
                elemento_sin_comillas = elemento.replace('"', "")
                res_list.append(elemento_sin_comillas)
            
            operadores = ["*", "^", "+", "-", "/", "(", ")"]

            operadores_reservados = []

            for elemento in res_list:
                if elemento in operadores:
                    operadores_reservados.append(elemento)

            print("\n[!] Operadores: ", operadores_reservados)

            for elemento in operadores_reservados:
                res_list.remove(elemento)


        for variable in variables:
            tabla[variable[0]] = variable[1]
        
        for key in tabla:
            tabla[key] = tabla[key].replace("E", "ε")
        
        if 'letter' in tabla:
            new_letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
            tabla['letter'] = tabla['letter'].replace("['a'-'z' 'A'-'Z']", new_letters)

        if 'digit' in tabla:
            new_digits = '(0|1|2|3|4|5|6|7|8|9)'
            tabla['digit'] = tabla['digit'].replace("['0'-'9']", new_digits)
        
        if 'digits' in tabla:
            new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
            tabla['digits'] = tabla['digits'].replace("digit+", new_digitsp)
        
        if 'space' in tabla: 
            new_space = '(_)(_)*'
            tabla['space'] = tabla['space'].replace("space", new_space)
        
        if 'endline' in tabla:
            new_endline = '(xyz)(xyz)*'
            tabla['endline'] = tabla['endline'].replace("endline", new_endline)
        
        if 'id' in tabla:
            new_letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
            new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
            new_space = '(_)(_)*'
            new_endline = '(xyz)(xyz)*'

            tabla['id'] = tabla['id'].replace("letter", new_letters)
            tabla['id'] = tabla['id'].replace("digits", new_digitsp)
            tabla['id'] = tabla['id'].replace("space", new_space)
            tabla['id'] = tabla['id'].replace("endline", new_endline)
            
        if 'number' in tabla:
            new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
            new_signs = "(@|~)"

            tabla['number'] = tabla['number'].replace("digits", new_digitsp)
            tabla['number'] = tabla['number'].replace("sign", new_signs)
        
        if 'sign' in tabla: 
            new_signs = "(@|~)"
            tabla['sign'] = tabla['sign'].replace("['+'|'-']", new_signs)
        
        if 'delim' in tabla:

            new_delims = "(≡|¥|§)"
            tabla['delim'] = tabla['delim'].replace("[' ''\\t''\\n']", new_delims)
        
        if 'ws' in tabla: 
            new_delimsp = "(≡|¥|§)(≡|¥|§)*"
            tabla['ws'] = tabla['ws'].replace("delim+", new_delimsp)

        if 'letterh' in tabla: 
            new_letters_h = '(A|B|C|D|E|F)'
            tabla['letterh'] = tabla['letterh'].replace("['A'-'F']", new_letters_h)
        
        if 'lettersh' in tabla: 
            new_letters_hs = '(A|B|C|D|E|F)(A|B|C|D|E|F)*'
            tabla['lettersh'] = tabla['lettersh'].replace("letterh+", new_letters_hs)
        
        if 'digite' in tabla: 
            new_digits_e = '(0|1|2|3|4|5|6|7|8|9)'
            tabla['digite'] = tabla['digite'].replace("['0'-'9']", new_digits_e)
        
        if 'digitse' in tabla: 
            new_digitsp_e = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
            tabla['digitse'] = tabla['digitse'].replace("digite+", new_digitsp_e)
        
        if 'hexdigit' in tabla:
            new_letters_h = '(A|B|C|D|E|F)'
            new_digits_e = '(0|1|2|3|4|5|6|7|8|9)'

            tabla['hexdigit'] = tabla['hexdigit'].replace("letterh", new_letters_h)
            tabla['hexdigit'] = tabla['hexdigit'].replace("digitse", new_digits_e)


        for key in tabla:
            tabla[key] = tabla[key].replace("[", "(")
            tabla[key] = tabla[key].replace("]", ")")

        listaA = []
        listaF = []

        for key in tabla:
            listaA.append(tabla[key])
        
        regex_final = ""
        alf_final = ""
        lista_temp = []
        lista_diccionarios = [] 
        lista_iniciales = [] 
        lista_finales = []


        for i in range(len(listaA)):
            regex = listaA[i]
            regex = regex.replace("?", "|ε")

            if "*" in regex:
                regex = regex.replace("*****************", "*")
                regex = regex.replace("****************", "*")
                regex = regex.replace("***************", "*")
                regex = regex.replace("**************", "*")
                regex = regex.replace("************", "*")
                regex = regex.replace("**********", "*")
                regex = regex.replace("********", "*")
                regex = regex.replace("******", "*")
                regex = regex.replace("*****", "*")
                regex = regex.replace("****", "*")
                regex = regex.replace("***", "*")
                regex = regex.replace("**", "*")

            regex = regex.replace("'", "")
            listaA[i] = regex

            bien = deteccion(regex)

            if bien: 

                alfI = alfabeto(regex)
                regexI = evaluar(regex)
                arbol = SintaxT(regexI, alfI)
                lista_diccionarios.append(arbol.dict) 
                lista_iniciales.append([arbol.EstadoInicial])
                lista_finales.append(arbol.EstadosAceptAFD)

            else: 
                print("[ERORR] Regex no valido")


        expr = "|".join(listaA)
        # print("Expresión unida: ", expr)
        reg = evaluar(expr)
        bien = deteccion(expr)

        if bien:
        
            regex_final = evaluar(expr)
            alf_final = alfabeto(regex_final)
        
        else: 
            print("[ERORR] Regex no valido")

        new_w = " "

        for dictionary in lista_diccionarios:
            for key in dictionary:
                if "≡" in dictionary[key]:
                    value = dictionary[key].pop("≡")
                    dictionary[key][new_w] = value
        
        new_t = "\t"
        for dictionary in lista_diccionarios:
            for key in dictionary:
                if "¥" in dictionary[key]:
                    value = dictionary[key].pop("¥")
                    dictionary[key][new_t] = value
        
        new_n = "\n"
        for dictionary in lista_diccionarios:
            for key in dictionary:
                if "§" in dictionary[key]:
                    value = dictionary[key].pop("§")
                    dictionary[key][new_n] = value
        
        new_p = "+"
        for dictionary in lista_diccionarios:
            for key in dictionary:
                if "@" in dictionary[key]:
                    value = dictionary[key].pop("@")
                    dictionary[key][new_p] = value
        
        new_m = "-"
        for dictionary in lista_diccionarios:
            for key in dictionary:
                if "~" in dictionary[key]:
                    value = dictionary[key].pop("~")
                    dictionary[key][new_m] = value

        SimuladorTxT(lista_diccionarios, lista_iniciales, lista_finales, archivo, res_list, operadores_reservados)