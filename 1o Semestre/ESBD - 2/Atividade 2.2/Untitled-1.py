class Elevador:
    def __init__(self):
        self.estado = Parado(self)

    def definir_estado(self, estado):
        self.estado = estado

    def solicitar_andar(self, andar):
        self.estado.solicitar_andar(andar)

    def emperrar(self):
        self.estado.emperrar()

    def em_manutencao(self):
        self.estado.em_manutencao()

    def reproduzir_musica(self):
        self.estado.reproduzir_musica()


class EstadoElevador:
    def __init__(self, elevador):
        self.elevador = elevador

    def solicitar_andar(self, andar):
        pass

    def emperrar(self):
        pass

    def em_manutencao(self):
        pass

    def reproduzir_musica(self):
        pass


class Parado(EstadoElevador):
    def solicitar_andar(self, andar):
        print("Elevador em movimento para o andar", andar)
        self.elevador.definir_estado(EmMovimento(self.elevador))

    def emperrar(self):
        print("Elevador emperrado")
        self.elevador.definir_estado(Emperrado(self.elevador))
        self.elevador.reproduzir_musica()


class EmMovimento(EstadoElevador):
    def solicitar_andar(self, andar):
        print("Elevador em movimento para o andar", andar)

    def em_manutencao(self):
        print("Elevador em manutenção")
        self.elevador.definir_estado(EmManutencao(self.elevador))

    def reproduzir_musica(self):
        print("Reproduzindo música no elevador")


class Emperrado(EstadoElevador):
    def em_manutencao(self):
        print("Elevador em manutenção")
        self.elevador.definir_estado(EmManutencao(self.elevador))

    def reproduzir_musica(self):
        print("Reproduzindo música no elevador")


class EmManutencao(EstadoElevador):
    def em_manutencao(self):
        print("Elevador em manutenção")


# Exemplo de uso
elevador = Elevador()
elevador.solicitar_andar(5)  # Elevador em movimento para o andar 5
elevador.emperrar()  # Elevador emperrado, reproduzindo música no elevador
elevador.em_manutencao()  # Elevador em manutenção
