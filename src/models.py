import database


class User:
    def __init__(self, userName, userEmail, userRole, userPassword):
        self.userName = userName
        self.userEmail = userEmail
        self.userRole = userRole
        self.userPassword = userPassword

        self.insert_user() # Insere o usuário no banco de dados

    def insert_user(self):
        self.userID = database.insert_user(self.userName, self.userEmail, self.userRole, self.userPassword)

    def update_user(self):
        pass

class Registro:
    def __init__(self, date, userID):
        self.date = date
        self.userId = userID # Quem sabe substituir pelo objeto User...

        self.cafe = None
        self.almoco = None
        self.janta = None
        self.lanche = None
        self.marmita = None


    def inserir_comensais(self, cafe, almoco, janta, lanche, marmita):
        self.cafe = cafe
        self.almoco = almoco
        self.janta = janta
        self.lanche = lanche
        self.marmita = marmita

    def alterar_comensais(self):
        pass


