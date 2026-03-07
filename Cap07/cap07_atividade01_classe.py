class Calculadora:
    def __init__(self, valor1, valor2):
        self._valor1 = valor1
        self._valor2 = valor2
    
    def soma(self):
        return self._valor1+self._valor2
    def sub(self):
        return self._valor1 - self._valor2
    def mult(self):
        return self._valor1 * self._valor2
    def div(self):
        return self._valor1 / self._valor2

