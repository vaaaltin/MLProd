from .interface import IRota

class RotaSegura(IRota):

    def atualiza_nivel_seguranca(self):
        print("O status da rota é: seguro")