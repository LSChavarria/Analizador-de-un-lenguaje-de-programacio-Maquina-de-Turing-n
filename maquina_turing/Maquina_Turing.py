class Datos():

    def __init__(self, cinta, automata, datos):
        self.__cinta = cinta
        self.__datos = datos
        self.__funciones_transicion = datos[automata]['funciones_transicion']
        self.__estados_finales = datos[automata]['conjunto_estados_finales']
        self.__gamma = datos[automata]['gamma']
        self.__blank = datos[automata]['blank']
        self.__estado_inicial = datos[automata]['estado_inicial']
        self.__automata = automata

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
    
    def get_automata(self):
        return self.__automata
    
    def set_cinta(self, cinta):
        self.__cinta = cinta

class Maquina_Turing(Datos):

    def __init__(self, cinta, automata, datos, p = 0):
        super().__init__(cinta, automata, datos)
        self.__estado = super().get_estado_inicial()
        self.__p = p
    
    def __left(self):
        self.__p -= 1
    
    def __rigth(self):
        self.__p += 1
    
    def __reubicar_p(self):
        sigma = self.__get_sigma()
        while sigma == self.get_blank:
            self.__rigth()
        self.__left()

    def __set_estado(self, estado):
        self.__estado = estado
    
    def __set_sigma(self, sigma):
        cinta = self.get_cinta()
        p = self.__p
        cinta[p] = sigma
        self.set_cinta(cinta)
    
    def __get_sigma(self):
        p = self.__p
        return self.get_cinta()[p]

    def __get_funcion_transicion(self, estado, sigma):
        funciones = self.get_funciones_transicion()
        try: 
            funcion = funciones[estado][sigma]
            return funcion
        except:
            return None
    
    def __get_estado_inicial(self, automata):
        return self.get_Datos()[automata]['estado_inicial']

    def __get_sigma_estado_inicial(self, automata, estado_inicial):
        return self.get_Datos()[automata]['funciones_transicion'][estado_inicial]
    
    def __get_sub_automata(self, sigma):
        gamma = super().get_gamma()
        for i, automatas in gamma:
            if automatas == None:
                continue
            for automata in automatas:
                #print(automata)
                aux = self.__get_estado_inicial(automata)
                aux = self.__get_sigma_estado_inicial(automata, aux)
                #print(i)
                for key in aux.keys():
                    if key == sigma:
                        #print("automata, i: ", automata, i)
                        return automata, i
        return None, None

    def __comprobar_funcion(self, estado, sigma):
        funcion = self.__get_funcion_transicion(estado, sigma)
        if funcion == None:
            return False, None
        else:
            return True, funcion

    def __delta(self, funcion):
        new_estado, new_sigma, x = funcion
        self.__set_estado(new_estado)
        self.__set_sigma(new_sigma)
        if x == "L":
            self.__left()
        elif x == "R":
            self.__rigth()

    def __get_opciones_sigma(self, estado):
        return self.get_funciones_transicion()[estado]

    def correr(self):
        cinta = self.get_cinta()
        while True:
            sigma = self.__get_sigma()
            #print(self.__p, sigma)
            valido, funcion = self.__comprobar_funcion(self.__estado, sigma)
            if not valido:
                sub_automata, sigma_automata = self.__get_sub_automata(sigma)
                #print("1 sub_automata, sigma_automata: ", sub_automata, sigma_automata)
                if sub_automata != None:
                    MT = Maquina_Turing(cinta, sub_automata, super().get_Datos(), self.__p)
                    retsultado_sub_automata, cinta, p = MT.correr()
                    #print("2 sub_automata, sigma_automata: ", self.__p, sub_automata, sigma_automata)
                    if retsultado_sub_automata:
                        self.set_cinta(cinta)
                        #sigma = sigma_automata
                        self.__p = p
                        self.__reubicar_p()
                        self.__set_sigma(sigma_automata)
                        #print(self.__p, self.__get_sigma(), cinta)
                        #valido, funcion = self.__comprobar_funcion(self.__estado, sigma)
                    else:
                        print("Error en el automata: ", self.get_automata(), self.__estado, sigma)
                        return False, self.get_cinta(), self.__p
                else:
                    print("Error al obtener la funcion: ", self.get_automata(), self.__estado, sigma)
                    print("Opciones: ", self.__get_opciones_sigma(self.__estado))
                    return False, self.get_cinta(), self.__p
            else:
                self.__delta(funcion)
                if self.__estado in self.get_estados_finales():
                    print(self.get_automata(), " valido")
                    return True, cinta, self.__p
