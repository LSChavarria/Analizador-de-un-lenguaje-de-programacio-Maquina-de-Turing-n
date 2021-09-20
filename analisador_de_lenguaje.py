from reglas_automatas.lectura_reglas import get_automata_gamma
from lectura_cinta.leer_cinta import get_cinta
from maquina_turing.Maquina_Turing import Maquina_Turing

if __name__ == '__main__':
    automatas, gamma = get_automata_gamma()
    cinta = get_cinta(gamma)
    #print(automatas, cinta, gamma)
    MT = Maquina_Turing(cinta, 'formato', automatas)
    resultado, cinta, p = MT.correr()
    print(cinta)
    if resultado:
        for i in cinta:
            if i != 'Æ€':
                resultado = False
                break
    if resultado:
        print("Cadena valida")
    else:
        print("Cadena invalida")