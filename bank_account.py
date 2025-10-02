
# Classe Compte
class Account:
    def __init__(self, name, balance=2000):
        self.name = name
        self.account_number = random.randint(1000000000, 9999999999)
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Dépôt de {amount} € → Solde: {self.balance} €")

    def withdraw(self, amount):
        if amount > self.balance:
            self.history.append(f"Échec retrait {amount} € (fonds insuffisants)")
        else:
            self.balance -= amount
            self.history.append(f"Retrait de {amount} € → Solde: {self.balance} €")

# Comptes de test
accounts = {
    "Ross": Account("Ross"),
    "Rachel": Account("Rachel")
}

# On simule quelques transactions
accounts["Ross"].deposit(500)
accounts["Ross"].withdraw(1150)

accounts["Rachel"].deposit(1500)
accounts["Rachel"].withdraw(50)
