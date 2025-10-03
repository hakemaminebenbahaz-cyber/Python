import random
from flask import Flask, render_template, request, redirect, url_for, session

# ================== FLASK APP ================== #
# Création de l'application Flask
app = Flask(__name__)
app.secret_key = "supersecret"  # nécessaire pour gérer les sessions (login/logout)


# ================== PARTIE 1 : CLASSE & COMPTES ================== #
class Account:
    """Classe représentant un compte bancaire."""

    def __init__(self, name, balance=2000):
        # Nom du titulaire
        self.name = name
        # Numéro de compte généré aléatoirement (10 chiffres)
        self.account_number = random.randint(1000000000, 9999999999)
        # Solde du compte
        self.balance = balance
        # Historique des opérations (list de strings)
        self.history = []

    def deposit(self, amount):
        """Effectue un dépôt et l'ajoute à l'historique"""
        self.balance += amount
        self.history.append(f"Dépôt de {amount} € → Solde: {self.balance} €")

    def withdraw(self, amount):
        """Effectue un retrait si le solde est suffisant"""
        if amount > self.balance:
            self.history.append(f"Échec retrait {amount} € (fonds insuffisants)")
        else:
            self.balance -= amount
            self.history.append(f"Retrait de {amount} € → Solde: {self.balance} €")


# ================== PARTIE 2 : CREATION DE COMPTES ================== #
# On crée deux comptes de test
accounts = {
    "Ross": Account("Ross"),
    "Rachel": Account("Rachel")
}

# On simule quelques transactions pour remplir l'historique
accounts["Ross"].deposit(500)
accounts["Ross"].withdraw(1150)

accounts["Rachel"].deposit(1500)
accounts["Rachel"].withdraw(50)


# ================== PARTIE 3 : ROUTES FLASK ================== #

# -------- LOGIN -------- #
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Page de login (admin/admin).
    Si l'utilisateur est correct → redirige vers le dashboard.
    Sinon → affiche un message d'erreur.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Identifiants incorrects")

    return render_template("login.html")


# -------- DASHBOARD -------- #
@app.route("/dashboard")
def dashboard():
    """
    Tableau de bord qui liste tous les comptes existants.
    Accessible uniquement si connecté.
    """
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", accounts=accounts)


# -------- PAGE COMPTE -------- #
@app.route("/account/<name>", methods=["GET", "POST"])
def account_page(name):
    """
    Page qui affiche le détail d’un compte.
    On peut y effectuer un dépôt ou un retrait.
    """
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    if request.method == "POST":
        action = request.form["action"]      # "deposit" ou "withdraw"
        amount = int(request.form["amount"]) # Montant saisi

        if action == "deposit":
            account.deposit(amount)
        elif action == "withdraw":
            account.withdraw(amount)

    return render_template("account.html", account=account)


# -------- HISTORIQUE -------- #
@app.route("/history/<name>")
def history(name):
    """
    Page qui affiche l’historique des transactions d’un compte.
    """
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    return render_template("history.html", account=account)


# ================== LANCEMENT APP ================== #
if __name__ == "__main__":
    # Lancement du serveur Flask en mode debug
    app.run(debug=True)
