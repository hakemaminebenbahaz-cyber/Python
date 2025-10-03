import random
from flask import Flask, render_template, request, redirect, url_for, session

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = "supersecret"  # nécessaire pour la session (login)

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
accounts["Ross"].withdraw(1150)import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecret"  

# ================== PARTIE 1 : CLASSE & COMPTES ================== #
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


# ================== PARTIE 2 : COMPTES ================== #
accounts = {
    "Ross": Account("Ross"),
    "Rachel": Account("Rachel")
}

# Historique de démo
accounts["Ross"].deposit(500)
accounts["Ross"].withdraw(1150)
accounts["Rachel"].deposit(1500)
accounts["Rachel"].withdraw(50)

# ================== PARTIE 2B : IDENTIFIANTS ================== #
users = {
    "Ross": {"password": "ross123", "account": accounts["Ross"]},
    "Rachel": {"password": "rachel123", "account": accounts["Rachel"]}
}


accounts["Rachel"].deposit(1500)
accounts["Rachel"].withdraw(50)
