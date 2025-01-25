import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, estado_inicial = (1, 1, ["sucio"] * 9)):
        self.x = list(estado_inicial)
        self.costo = 0

    def accion_legal(self, accion):
        return accion in ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]
    def transición(self, accion):
        if not self.accion_legal(accion):
            raise ValueError(f"La acción {accion} no es legal para el estado {self.x}")
        
        piso, cuarto, cuartos = self.x

        if accion == "ir_derecha":
            self.x[1] += 1
            self.costo += 1
        elif accion == "ir_izquierda":
            self.x[1] -= 1
            self.costo += 1
        elif accion == "subir":
            self.x[0] += 1
            self.costo += 2
        elif accion == "bajar":
            self.x[0] -= 1
            self.costo += 2
        elif accion == "limpiar":
            index = (piso - 1) * 3 + (cuarto - 1)
            cuarto[index] = "limpio"
            self.costo += 0.5
        elif accion == "nada":
            pass
    
    def percepción(self):
        piso, cuarto, cuartos = self.x
        index = (piso - 1) * 3 + (cuarto - 1)
        return piso, cuarto, cuartos[index]
    

class AgenteReactivo(entornos_o.Agente):
    def __init__(self):
        self.modelo = [1, 1, ["sucio"] * 9]

    def programa(self, percepcion):
        piso, cuarto, situacion = percepcion
        self.modelo[0] = piso
        self.modelo[1] = cuarto
        index = (piso - 1) * 3 + (cuarto - 1)
        self.modelo[2][index] = situacion

        cuartos = self.modelo[2]

        if all(c == "limpio" for c in self.modelo[2]):
            return "nada"
        elif situacion == "sucio":
            return "limpiar"
        elif cuarto < 3 and cuartos[(piso - 1) * 3 + cuarto] == "sucio":
            return "ir_derecha"
        elif cuarto > 1 and cuartos[(piso - 1) * 3 + cuarto - 2] == "sucio":
            return "ir_izquierda"
        elif piso < 3 and cuarto == 3:
            return "subir"
        elif piso > 1 and cuarto == 1:
            return "bajar"
        else:
            return "nada"
        



