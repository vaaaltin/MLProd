#product
class Cliente:
    def client(self)-> None:
        raise NotImplementedError
#creator
class ClienteFactory(Cliente):
    def createClient(self) -> Cliente:
        raise NotImplementedError

#concrete product
class ClienteFisico(Cliente):
    # raise NotImplementedError
    def cliente(self):
        print('Cliente Fisico')

#concrete product
class ClienteJuridico(Cliente):
    # raise NotImplementedError
    def cliente(self):
        print('Cliente Juridico')

#concrete creator
class ClienteJuridicoFactory(ClienteFactory):
    def factoryMethod(self) -> Cliente:
        return ClienteJuridico()


#concrete creator
class ClienteFisicoFactory(ClienteFactory):
    def factoryMethod(self) -> Cliente:
        return ClienteFisico()
    

if __name__ == "__main__":
    obj1 = ClienteJuridicoFactory().factoryMethod()
    obj1.cliente()

    obj2 = ClienteFisicoFactory().factoryMethod()
    obj2.cliente()