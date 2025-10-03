
import random
from flask import Flask, render_template, request,redirect, url_for, session

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
accounts["Ross"].withdraw(1150)

accounts["Rachel"].deposit(1500)
accounts["Rachel"].withdraw(50)

# ================= ROUTES FLASK ================= #
# Page de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # login simple (admin / admin)
        if username == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Identifiants incorrects")

    return render_template("login.html")


# Tableau de bord (liste des comptes)
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", accounts=accounts)


# Page d’un compte
@app.route("/account/<name>", methods=["GET", "POST"])
def account_page(name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    if request.method == "POST":
        action = request.form["action"]
        amount = int(request.form["amount"])

        if action == "deposit":
            account.deposit(amount)
        elif action == "withdraw":
            account.withdraw(amount)

    return render_template("account.html", account=account)


# Historique
@app.route("/history/<name>")
def history(name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    return render_template("history.html", account=account)


if __name__ == "__main__":
    app.run(debug=True)
