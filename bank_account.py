import random
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

# ================== ROUTES ================== #

# -------- LOGIN -------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["logged_in"] = True
            session["user"] = username
            return redirect(url_for("account_page", name=username))
        else:
            return render_template("login.html", error="Identifiants incorrects")
    return render_template("login.html")

# -------- ACCOUNT -------- #
@app.route("/account/<name>", methods=["GET", "POST"])
def account_page(name):
    if not session.get("logged_in") or session.get("user") != name:
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    error = None
    if request.method == "POST":
        action = request.form.get("action")
        amount = int(request.form["amount"])

        if action == "deposit":
            account.deposit(amount)
        elif action == "withdraw":
            if amount > account.balance:
                error = "Fonds insuffisants ! Retrait impossible."
                account.history.append(f"Échec retrait {amount} € (fonds insuffisants)")
            else:
                account.withdraw(amount)
        else:
            error = "Veuillez choisir une opération valide."

    return render_template("account.html", account=account, error=error)

# -------- HISTORY -------- #
@app.route("/history/<name>")
def history(name):
    if not session.get("logged_in") or session.get("user") != name:
        return redirect(url_for("login"))

    account = accounts.get(name)
    if not account:
        return "Compte introuvable", 404

    return render_template("history.html", account=account)

# -------- LOGOUT -------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================== LANCEMENT ================== #
if __name__ == "__main__":
    app.run(debug=True)
