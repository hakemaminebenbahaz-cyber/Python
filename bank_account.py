import random

class Account:
    def __init__(self, name, balance=2000):
        self.name = name
        self.account_number = random.randint(1000000000, 9999999999)  # numéro aléatoire à 10 chiffres
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def dump(self):
        print(f"{self.name}, {self.account_number}, {self.balance}")

# Création des comptes
ross_account = Account("Ross")
rachel_account = Account("Rachel")

# Quelques opérations
ross_account.deposit(500)
ross_account.withdraw(1150)

rachel_account.deposit(1500)
rachel_account.withdraw(50)

# Affichage final
ross_account.dump()
rachel_account.dump()
