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
