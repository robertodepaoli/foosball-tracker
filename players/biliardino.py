class Biliardino():

    def __init__(self):
        self.stecche_rosse = SetStecche('rosso')
        self.stecche_blu = SetStecche('blu')


class Stecca(): 
    def __init__(self, id, numero_pitotini, colore, shift = 0, angolo = 0):
        self.id = f'{id}_{colore}'
        self.shift = shift
        self.angolo = angolo
        self.pitotini = []
        for id_pit, pitotino in enumerate(range(numero_pitotini)):
            self.pitotini.append(Pitotino(f'{id}_{colore}_{id_pit}'))
    
class Portiere(Stecca):   
    def __init__(self, colore):
        Stecca.__init__(self, 'portiere', 1, colore)

class Difensore(Stecca): 
    def __init__(self, colore):
        Stecca.__init__(self, 'difensore', 2, colore)

class Centrocampo(Stecca):  
    def __init__(self, colore):
        Stecca.__init__(self, 'centrocampo', 5, colore)

class Attacco(Stecca): 
    def __init__(self, colore):
        Stecca.__init__(self, 'attacco', 3, colore)

class SetStecche():
    def __init__(self, colore):
        self.colore = colore
        self.portiere = Portiere(colore)
        self.difensore = Difensore(colore)
        self.centrocampo = Centrocampo(colore)
        self.attacco = Attacco(colore)


class Pitotino():
    
    def __init__(self, id, x=0, y=0):
        self.id = id
        self.x = x
        self.y = y
    
    def update(self, x, y):
        self.x = x
        self.y = y

