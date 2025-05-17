import entornos_o
from random import choice, random
import copy

__author__ = 'francisco_yanez'

class nuevecuartos(entornos_o.Entorno):
    def __init__(self, x0=[0,0, [["sucio"] * 3 for _ in range(3)]]):
        self.x = x0
        self.costo = 0
    
    def accion_legal(self, accion):
        return accion in ("ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("Accion no legal...")
        
        piso, cuarto, estado = self.x

        if accion == "limpiar":
            self.costo += 1
            estado[piso][cuarto] = "limpio"
        elif accion == "ir_derecha":
            self.costo += 2
            if cuarto < 2:
                self.x[1] += 1
        elif accion == "ir_izquierda":
            self.costo += 2
            if cuarto > 0:
                self.x[1] -= 1
        elif accion == "subir":
            self.costo += 3
            if piso < 2:
                self.x[0] += 1
        elif accion == "bajar":
            self.costo += 3
            if piso > 0:
                self.x[0] -= 1
        elif accion == "nada":
            pass
    
    def percepcion(self):
        piso, cuarto, estado = self.x
        return piso, cuarto, estado[piso][cuarto]
    

class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, acciones):
        self.acciones = acciones
        
    def programa(self, _):
        return choice(self.acciones)
    

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self):
        self.modelo = [[ "sucio" for _ in range(3)] for _ in range(3)]
        self.ubicacion = (0, 0)  # piso, cuarto

    def programa(self, percepcion):
        piso, cuarto, estado_actual = percepcion
        self.ubicacion = (piso, cuarto)

        # Actualizar el modelo con la percepción actual
        self.modelo[piso][cuarto] = estado_actual

        # Si el cuarto está sucio, limpiarlo
        if estado_actual == "sucio":
            return "limpiar"

        # Buscar el siguiente cuarto sucio en el mismo piso
        for i in range(3):
            if self.modelo[piso][i] == "sucio":
                if i < cuarto:
                    return "ir_izquierda"
                elif i > cuarto:
                    return "ir_derecha"

        # Si no hay cuartos sucios en el piso actual, subir o bajar
        for p in range(3):
            for c in range(3):
                if self.modelo[p][c] == "sucio":
                    if p > piso:
                        return "subir"
                    elif p < piso:
                        return "bajar"

        # Si todo está limpio, no hacer nada
        return "nada"
    
class NueveCuartosCiego(nuevecuartos):
    def percepcion(self):
        piso, cuarto, _ = self.x
        return (piso, cuarto)

class AgenteRacionalCiego(entornos_o.Agente):
    def __init__(self):
        self.modelo = [["sucio"] * 3 for _ in range(3)]
        self.ubicacion = (0, 0)

    def programa(self, percepcion):
        piso, cuarto = percepcion
        self.ubicacion = (piso, cuarto)

        # Si elcuarto está sucio, limpiar
        if self.modelo[piso][cuarto] == "sucio":
            self.modelo[piso][cuarto] = "limpio"
            return "limpiar"

        # Ir al siguiente cuarto sucio según el modelo
        for p in range(3):
            for c in range(3):
                if self.modelo[p][c] == "sucio":
                    if p > piso:
                        return "subir"
                    elif p < piso:
                        return "bajar"
                    elif c > cuarto:
                        return "ir_derecha"
                    elif c < cuarto:
                        return "ir_izquierda"

        return "nada"  # Todo está limpio
    

class NueveCuartosEstocastica(nuevecuartos):

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("Acción no legal…")
        
        piso, cuarto, estado = self.x
        r = random()

        if accion == "limpiar":
            self.costo += 1                       # siempre cuesta 1
            if r < 0.8:                           # 80 %: limpia
                estado[piso][cuarto] = "limpio"

        elif accion in ("ir_derecha", "ir_izquierda", "subir", "bajar"):
            if   r < 0.8:       accion_real = accion         
            elif r < 0.9:       accion_real = "nada"                      
            else:
                # acción aleatoria legal distinta de la intencionada
                otras = [a for a in ("ir_derecha","ir_izquierda","subir",
                                     "bajar","limpiar","nada")
                         if a != accion]
                accion_real = choice(otras)

            # ejecutar la acción REAL y sumar su costo correspondiente
            if accion_real == "ir_derecha":
                self.costo += 2
                if cuarto < 2:
                    self.x[1] += 1
            elif accion_real == "ir_izquierda":
                self.costo += 2
                if cuarto > 0:
                    self.x[1] -= 1
            elif accion_real == "subir":
                self.costo += 3
                if piso < 2:
                    self.x[0] += 1
            elif accion_real == "bajar":
                self.costo += 3
                if piso > 0:
                    self.x[0] -= 1
            elif accion_real == "limpiar":
                self.costo += 1
                # 80 % de éxito / 20 % fallo para la limpieza aleatoria
                if random() < 0.8:
                    self.x[2][piso][cuarto] = "limpio"

        elif accion == "nada":
            pass

class AgenteRacionalEstocastico(entornos_o.Agente):
    def __init__(self):
        self.modelo = [["sucio"] * 3 for _ in range(3)]
        self.ubic = (0, 0)

    def programa(self, percepcion):
        piso, cuarto, estado = percepcion
        self.ubic = (piso, cuarto)
        self.modelo[piso][cuarto] = estado

        # 1. Si está sucio, limpiamos
        if estado == "sucio":
            return "limpiar"

        # 2. Buscar el siguiente cuarto sucio
        for p in range(3):
            for c in range(3):
                if self.modelo[p][c] == "sucio":
                    if p > piso:
                        return "subir"
                    if p < piso:
                        return "bajar"
                    if c > cuarto:
                        return "ir_derecha"
                    if c < cuarto:
                        return "ir_izquierda"

        # 3. Si según mi modelo todo está limpio, no hacemos nada
        return "nada"


def test():
    x0 = [0, 0, [["sucio"] * 3 for _ in range(3)]]

    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(nuevecuartos(copy.deepcopy(x0)), 
                         AgenteAleatorio(['ir_derecha', 'ir_izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)

    print("\nPrueba del entorno con un agente reactivo basado en modelo")
    entornos_o.simulador(nuevecuartos(copy.deepcopy(x0)), 
                         AgenteReactivoModeloNueveCuartos(),
                         200)
    
    print("\n--- Prueba del entorno CIEGO con agente ALEATORIO ---")
    entornos_o.simulador(
        NueveCuartosCiego(copy.deepcopy(x0)),
        AgenteAleatorio(["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]),
        200
    )

    print("\n--- Prueba del entorno CIEGO con agente RACIONAL ---")
    entornos_o.simulador(
        NueveCuartosCiego(copy.deepcopy(x0)),
        AgenteRacionalCiego(),
        200
    )

    print("\n Entorno Estocástico con agente ALEATORIO")
    entornos_o.simulador(
        NueveCuartosEstocastica(copy.deepcopy(x0)),
        AgenteAleatorio(['ir_derecha','ir_izquierda','subir','bajar','limpiar','nada']),
        200    
    )

    print("\n Entorno Estocástico con agente RACIONAL")
    entornos_o.simulador(
        NueveCuartosEstocastica(copy.deepcopy(x0)),
        AgenteRacionalEstocastico(),
        200
    )

if __name__ == "__main__":
    test()

