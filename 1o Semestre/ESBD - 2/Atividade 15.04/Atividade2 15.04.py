from abc import ABC, abstractmethod

class MineracaoDados(ABC):
    def minerar_dados(self) -> None:
        self.abrir()
        self.extrair()
        self.parsear()
        self.realizarAnalise()
        self.enviarRelatorio()
        self.fechar()
        
    def enviarRelatorio(self) -> None:
        print('enviando relatorio')
    
    def realizarAnalise(self) -> None:
        print('realizar analise')

    @abstractmethod
    def abrir(self) -> None:
        pass

    @abstractmethod
    def extrair(self) -> None:
        pass

    @abstractmethod
    def parsear(self) -> None:
        pass

    @abstractmethod
    def fechar(self) -> None:
        pass


class MineracaoDadosCSV(MineracaoDados):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    def abrir(self) -> None:
        print("abrindo arquivo csv")
    
    def extrair(self) -> None:
        print("extrair csv")

    def parsear(self) -> None:
        print("parsear csv")

    def fechar(self) -> None:
        print("fechar csv")



class MineracaoDadosXML(MineracaoDados):
    """
    Usually, concrete classes override only a fraction of base class'
    operations.
    """

    def abrir(self) -> None:
        print("abrindo arquivo xml")
    
    def extrair(self) -> None:
        print("extrair xml")

    def parsear(self) -> None:
        print("parsear xml")

    def fechar(self) -> None:
        print("fechar xml")


def client_code(classe_abstrata: MineracaoDados) -> None:
    classe_abstrata.minerar_dados()


if __name__ == "__main__":
    client_code(MineracaoDadosCSV())
    print("")

    client_code(MineracaoDadosXML())