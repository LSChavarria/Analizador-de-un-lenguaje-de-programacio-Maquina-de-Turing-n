import pprint
import os
from io import open 
from string import ascii_lowercase, digits

def lectura(path):
    archivo = open(path, "r")
    contenido = archivo.readlines()
    archivo.close()
    return contenido

def conjunto_valido(start, end, contenedor = "{}"):
    return start == contenedor[0] and end == contenedor[-1]

def extraer_conjuntos(conjunto, separador = ","):
    conjunto = conjunto.split(separador)
    conjunto = [i.strip() for i in conjunto]
    return conjunto

def separar_llave_valor(contenido):
    diccionario = {}
    for i in contenido:
        data = i.split("=")
        if len(data) != 2:
            continue
        data = [cadena.strip(" \n") for cadena in data]
        diccionario[data[0]] = data[1]
    return diccionario
    
def extraer_ascii_digits(value):
    value = value[1:-1].split("_")
    if value[0].isalpha():
        conjunto_valores = ascii_lowercase 
    else:
        conjunto_valores = digits
    start = list(conjunto_valores).index(value[0])
    end = list(conjunto_valores).index(value[1]) + 1
    return [conjunto_valores[i] for i in range(start, end)]

def preparar_gamma(gamma):
    new_gamma = []
    for i in gamma:
        if i[0] == "(" and i[-1] == ")":
            elementos = extraer_conjuntos(i[1:-1], ";")
            sigma = elementos[0]
            elementos = elementos[1:]
            new_gamma.append([sigma, elementos])
        else:
            new_gamma.append([i, None])
    return new_gamma

def extraer_funciones_transicion(funciones):
    funciones_transicion = {}
    for key in funciones:
        estado, t = extraer_conjuntos(key[2:-1])
        funcion = extraer_conjuntos(funciones[key][1:-1])
        try:
            dict = funciones_transicion[estado]
        except:
            dict = {}
        dict[t] = funcion
        funciones_transicion[estado] = dict

    return funciones_transicion

def obtener_llave_subconjunto(funciones_transicion, subconjuntos_sigma):
    llaves_subconjuntos = []
    for key in funciones_transicion:
        for subkey in funciones_transicion[key]:
            for key_sub_sigma in subconjuntos_sigma:
                if subkey == key_sub_sigma:
                    llaves_subconjuntos.append([key, subkey])
                    break
    return llaves_subconjuntos

def distribuir_sub_func_trans(llaves_subconjuntos, funciones_transicion, subcadenas):
    for key, subkey in llaves_subconjuntos:
        new_estado, new_sigma, new_cambio = funciones_transicion[key][subkey]
        new_subkeys = subcadenas[subkey]
        for new_subkey in new_subkeys:
            funciones_transicion[key][new_subkey] = [new_estado, new_sigma, new_cambio]
    return funciones_transicion

def distribuir_sub_gamma(gamma, subconjuntos_sigma):
    new_gamma = []
    for i, j in gamma:
        try:
            for sigma in subconjuntos_sigma[i]:
                new_gamma.append([sigma, j])
        except:
            new_gamma.append([i,j])
    return new_gamma

def dividir_contenido(contenido):
    estados = []
    sigma = []
    gamma = []
    subconjuntos_sigma = {}
    estado_inicial = None
    conjunto_estados_finales = []
    blank = None
    funciones_transicion = {}
    subcadenas_funciones_transicion = {}

    diccionario = separar_llave_valor(contenido)
    
    for key in diccionario:
        value = diccionario[key]
        if key == "Q" and conjunto_valido(value[0], value[-1], "()"):
            estados = extraer_conjuntos(value[1:-1])
        elif key == "Sigma" and conjunto_valido(value[0], value[-1]):
            sigma = extraer_conjuntos(value[1:-1])
        elif key == "Gamma" and conjunto_valido(value[0], value[-1]):
            gamma = extraer_conjuntos(value[1:-1])
            gamma = preparar_gamma(gamma)
        elif key == "S":
            estado_inicial = value.strip()
        elif key == "F" and conjunto_valido(value[0], value[-1]):
            conjunto_estados_finales = extraer_conjuntos(value[1:-1])
        elif key == "Blank":
            blank = value.strip()
        elif key[0] == "_":
            subcadenas_funciones_transicion[key] = extraer_conjuntos(value[1:-1])
        elif key.islower() and conjunto_valido(value[0], value[-1], "[]"):
            subconjuntos_sigma[key] = extraer_ascii_digits(value)
        elif key.islower() and conjunto_valido(value[0], value[-1]):
            subconjuntos_sigma[key] = extraer_conjuntos(value[1:-1])
        elif key.islower():
            subconjuntos_sigma[key] = [value.strip()]
        elif key.startswith("D(") and key[-1] == ")":
            funciones_transicion[key] = value
        else:
            print("Error al leer la configuracion de la maquina")
    
    funciones_transicion = extraer_funciones_transicion(funciones_transicion)

    llaves_subconjuntos = obtener_llave_subconjunto(funciones_transicion, subcadenas_funciones_transicion)

    funciones_transicion = distribuir_sub_func_trans(llaves_subconjuntos, funciones_transicion, subcadenas_funciones_transicion)

    llaves_subconjuntos = obtener_llave_subconjunto(funciones_transicion, subconjuntos_sigma)

    funciones_transicion = distribuir_sub_func_trans(llaves_subconjuntos, funciones_transicion, subconjuntos_sigma)
    
    old_gamma = gamma

    gamma = distribuir_sub_gamma(gamma, subconjuntos_sigma)

    elementos_MT = {
        'estados': estados,
        'sigma' : sigma,
        'gamma' : gamma,
        'old_gamma' : old_gamma,
        'subconjuntos_sigma' : subconjuntos_sigma,
        'estado_inicial' : estado_inicial,
        'conjunto_estados_finales' : conjunto_estados_finales,
        'blank' : blank,
        'funciones_transicion' : funciones_transicion,
        'subcadenas_funciones_transicion' : subcadenas_funciones_transicion
    }
    return elementos_MT

def funciones_transicion(direc):
    Maquinas_Turing = {}
    archivos = [i for i in os.listdir(direc) if i.endswith(".txt")]
    for i in archivos:
        path = os.path.join(direc, i)
        i = i[:-4]
        contenido = lectura(path)
        contenido = dividir_contenido(contenido)
        Maquinas_Turing[i] = contenido
    return Maquinas_Turing

def gamma(Maquinas_Turing):
    Gamma = []
    for key in Maquinas_Turing:
        sub_gamma = Maquinas_Turing[key]['gamma']
        sub_gamma = [i[0] for i in sub_gamma]
        Gamma = Gamma + sub_gamma
    Gamma = set(Gamma)
    return list(Gamma)

def get_automata_gamma():
    direc =  r"C:\Users\sebas\Desktop\MT\Maquina_Turing\reglas_automatas\reglas"
    automata = funciones_transicion(direc)
    Gamma = gamma(automata)
    return automata, Gamma

if __name__ == '__main__':
    Maquinas_Turing, Gamma = get_automata_gamma()
    pp = pprint.PrettyPrinter()
    pp.pprint(Maquinas_Turing)
    print(Gamma)
    