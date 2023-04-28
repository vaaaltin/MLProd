from abc import ABC, abstractmethod

# padrão state
class ElevadorState(ABC):
    @abstractmethod
    def subir(self):
        pass

    @abstractmethod
    def descer(self):
        pass

    @abstractmethod
    def parar(self):
        pass

class SubindoState(ElevadorState):
    def subir(self):
        print("O elevador já está subindo.")
        return self

    def descer(self):
        print("O elevador não pode descer pois está subindo")
        return self

    def parar(self):
        print("O elevador está parando.")
        return ParadoState()
    
class DescendoState(ElevadorState):
    def subir(self):
        print("O elevador não pode subir pois está descendo.")
        return self
    
    def descer(self):
        print("O elevador já está descendo.")
        return self
    
    def parar(self):
        print("O elevador está parando.")
        return ParadoState()

class ParadoState(ElevadorState):
    def subir(self):
        print("O elevador está subindo.")
        return SubindoState()

    def descer(self):
        print("O elevador está descendo.")
        return DescendoState()
    
    def parar(self):
        print("O elevador já está parado.")

class Elevador:
    def __init__(self):
        self.current_floor = 1
        self.state = ParadoState()

    def set_state(self, state):
        self.state = state
    
    def subir(self):
        self.current_floor += 1
        self.state = self.state.subir()
        print(f"O elevador está no elevador {self.current_floor}")
    
    def descer(self):
        self.current_floor -= 1
        self.state = self.state.descer()
        print(f"O elevador está no andar {self.current_floor}")

    def parar(self):
        self.state = self.state.parar()
        print("O elevador parou.")

#padrão observer
class ElevatorObserver:
    def __init__(self, elevador):
        self.elevador = elevador

    def update(self, evento):
        if evento == "manutencao":
            print("O elevador está em manutencao")
        elif evento == "problema":
            print("O elevador está com problema. Chame assistência.")

class ElevatorSubject:
    def __init__(self):
        self.observadores = []
    
    def attach(self, observador):
        self.observadores.append(observador)

    def detach(self, observador):
        self.observadores.remove(observador)

    def notify(self, evento):
        for observador in self.observadores:
            observador.update(evento)


#padrão Flyweight
class MusicaElevador:
    def __init__(self, musica):
        self.musica = musica

class MusicaElevadorFactory:
    def __init__(self):
        self.cache_musica = {}
    
    def get_music(self, musica):
        if musica not in self.cache_musica:
            self.cache_musica[musica] = MusicaElevador(musica)
        return self.cache_musica[musica]


if __name__ == '__main__':
    #criando objecto elevador
    elevador = Elevador()

    #criando observadores dos elevadores
    maintenance_observer = ElevatorObserver(elevador)
    problema_observador = ElevatorObserver(elevador)

    #criando sujeito elevador e incluindo os observadores
    elevador_subject = ElevatorSubject()
    elevador_subject.attach(maintenance_observer)
    elevador_subject.attach(problema_observador)

    #setando o estado do elevador para subindo
    elevador.set_state(SubindoState())

    #movendo o elevador para cima
    elevador.subir()
    elevador.subir()

    #setando o estado do elevador para descendo
    elevador.set_state(DescendoState())
    
    #movendo o elevador para baixo
    elevador.descer()

    #parado o elevador
    elevador.parar()

    #notificando os observadores um evento de manutenção
    elevador_subject.notify("manutencao")

    #notificando os observador um evento de problema
    elevador_subject.notify("problema")

    #tocando musica usando o padrao flyweight
    music_factory = MusicaElevadorFactory()
    musica1 = music_factory.get_music("Classico")
    musica2 = music_factory.get_music("Rock")
    musica3 = music_factory.get_music("Heavy Metal")

    print(musica1.musica)
    print(musica2.musica)
    print(musica3.musica)