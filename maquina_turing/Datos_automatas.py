class Datos():

    def __init__(self, cinta, automata, datos):
        self.__cinta = cinta
        self.__datos = datos
        self.__funciones_transicion = datos[automata]['funciones_transicion']
        self.__estados_finales = datos[automata]['conjunto_estados_finales']
        self.__gamma = datos[automata]['gamma']
        self.__blank = datos[automata]['blank']
        self.__estado_inicial = datos[automata]['estado_inicial']

    def get_Datos(self):
        return self.__datos

    def get_cinta(self):
        return self.__cinta
    
    def get_funciones_transicion(self):
        return self.__funciones_transicion
    
    def get_estados_finales(self):
        return self.__estados_finales
    
    def get_gamma(self):
        return self.__gamma
    
    def get_blank(self):
        return self.__blank

    def get_estado_inicial(self):
        return self.__estado_inicial
    
    def set_cinta(self, cinta):
        self.__cinta = cinta