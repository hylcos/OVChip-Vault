import requests
from flask import Flask, render_template, request, redirect, session, url_for
from ovchipcard.api import Api

app = Flask(__name__)
SESSION_TYPE = "redis"
app.secret_key = "F00DDEAD"
app.config.from_object(__name__)

accounts = {}


# account = Api.login("Hylcoss", "^3b9YxZTA$jG#nv5s")
# cards = account.cards
# card = cards[1]
# trans = card.transactions
# for t in trans:
#     timestamp = datetime.fromtimestamp(t.transactionDateTime)
#     print(timestamp)

@app.route('/card/<int:id>/routes')
def get_routes(id):
    account_id = session.get("account")
    if not account_id or account_id not in accounts.keys():
        return redirect(url_for("login", message="Unauthorized"))
    account = accounts[account_id]
    card = [c for c in account.cards if int(c.mediumId) == id][0]
    routes = card.routes
    print(routes)
    return render_template("routes.html", routes=routes)


@app.route('/card/<int:id>/transactions')
def get_transactions(id):
    account_id = session.get("account")
    if not account_id or account_id not in accounts.keys():
        return redirect(url_for("login", message="Unauthorized"))
    account = accounts[account_id]
    card = [c for c in account.cards if int(c.mediumId) == id][0]
    trans = card.transactions
    return render_template("trans.html", trans=trans)


@app.route('/cards')
def get_cards():
    account_id = session.get("account")
    if not account_id or account_id not in accounts.keys():
        return redirect(url_for("login", message="Unauthorized"))
    account = accounts[account_id]
    return render_template("cards.html", cards=account.cards)


@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            account = Api.login(request.form["username"], request.form["password"])
            session["account"] = account.authCode
            accounts[account.authCode] = account
            return redirect(url_for("get_cards"))
        except requests.exceptions.HTTPError as e:
            return render_template("login.html", message="Invalid username and/or password")
    else:
        message = request.values.get("message", None)
        if message:
            return render_template("login.html", message=message)
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
