from bot import Bot

class MiBot(Bot):

    def __init__(self):
        super().__init__() # Si borras esta línea rompes el bot no lo hagas :(
        # Crea tus variables para tu bot aquí y recuerda que les tienes que poner self.
        self.ejemplo_variable = 0

    def behavior(self):
        # Este método se ejecutará tras cada actualización del juego
        # introduce tu comportamiento aquí y mucha suerte
        self.go_right() # Yendo a la derecha como Mario
