from abc import ABC, abstractmethod


class Arquivo(ABC):
    def template_method(self) -> None:
        """
        The template method defines the skeleton of an algorithm.
        """

        self.abrir()


    @abstractmethod
    def abrir(self) -> None:
        pass




class ArquivoCSV(Arquivo):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    def abrir(self) -> None:
        print("ConcreteClass1 says: Implemented Operation1")



class ArquivoXML(Arquivo):
    """
    Usually, concrete classes override only a fraction of base class'
    operations.
    """

    def abrir(self) -> None:
        print("ConcreteClass2 says: Implemented Operation1")
def client_code(abstract_class: Arquivo) -> None:
    """
    The client code calls the template method to execute the algorithm. Client
    code does not have to know the concrete class of an object it works with, as
    long as it works with objects through the interface of their base class.
    """

    # ...
    abstract_class.template_method()
    # ...


if __name__ == "__main__":
    print("Same client code can work with different subclasses:")
    client_code(ArquivoCSV())
    print("")

    print("Same client code can work with different subclasses:")
    client_code(ArquivoXML())