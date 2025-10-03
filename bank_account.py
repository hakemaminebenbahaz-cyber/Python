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