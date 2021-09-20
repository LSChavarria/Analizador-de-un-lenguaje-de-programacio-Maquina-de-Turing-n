from string import ascii_lowercase, digits

def lectura(path):
    archivo = open(path, "r")
    contenido = archivo.readlines()
    archivo.close()
    return contenido

def limpiar_espacios_linea(contenido, espacios = [" ", "\t", "\n"]):
    for espacio in espacios:
        nuevo_contenido = []
        for i in contenido:
            if espacio in i:
                aux = [j for j in i.split(espacio) if j != '']
                for j in aux:
                    nuevo_contenido.append(j)
            else:
                nuevo_contenido.append(i)
        contenido = nuevo_contenido
    return contenido
    
def separar_sub_cinta(contenido, gamma):
    new_contenido = []
    aux = ""
    for i in contenido:
        if i in ascii_lowercase or i in digits:
            aux += i
        else:
            if aux in gamma:
                new_contenido.append(aux)
            else:
                new_contenido += list(aux)
            aux = ""
            new_contenido.append(i)
    return new_contenido
    

def separar_cinta(contenido, gamma):
    new_contenido = []
    for i in contenido:
        if i in gamma:
            new_contenido.append(i)
        else:
            new_contenido += separar_sub_cinta(i, gamma)
    return new_contenido

def get_cinta(gamma):
    direc =  r"C:\Users\sebas\Desktop\MT\Maquina_Turing\Cadena.txt"
    contenido = lectura(direc)
    contenido = limpiar_espacios_linea(contenido)
    contenido = separar_cinta(contenido, gamma)
    return contenido

if __name__ == '__main__':
    gamma = ['r', 'h', '(', 'Æ€', 'e', 's', 'w', 'nombre', 'g', 'j', '-', 'instrucciÃ³n', 'iniciar', 'c', '2', '*', '5', '3', 'identificador', '^', '.', ':', 'valores', '/', 'q', '7', 'd', 'listado-de-instrucciones', 'imprimir', 'k', '6', 'o', '0', 'm', '4', '+', 'i', ')', 't', 'expresiÃ³n_aritmÃ©tica', 'a', '1', 'u', 'b', 'programa', 'x', 
                'f', '9', 'l', 'p', 'v', ';', '8', 'n', 'leer', 'y', 'z', 'terminar']
    get_cinta(gamma)