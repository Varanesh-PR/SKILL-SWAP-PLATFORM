from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATA ----------------
users = [
    {"username": "admin", "password": "123", "teach_skill": "python ai", "learn_skill": "java"},
    {"username": "john", "password": "123", "teach_skill": "java web", "learn_skill": "python"},
    {"username": "alice", "password": "123", "teach_skill": "ml data science", "learn_skill": "python"}
]

messages = []

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for u in users:
            if u["username"] == request.form["username"] and u["password"] == request.form["password"]:
                session["user"] = u["username"]
                return redirect("/dashboard")
        return "Invalid Login"
    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users.append({
            "username": request.form["username"],
            "password": request.form["password"],
            "teach_skill": request.form["teach"],
            "learn_skill": request.form["learn"]
        })
        return redirect("/")
    return render_template("register.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", users=users)


# ---------------- AI MATCH ----------------
@app.route("/match")
def match():
    user_name = session["user"]
    current = next(u for u in users if u["username"] == user_name)

    def similarity(a, b):
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())
        return len(a_words & b_words)

    results = []
    for u in users:
        if u["username"] != user_name:
            score = similarity(current["learn_skill"], u["teach_skill"]) + \
                    similarity(current["teach_skill"], u["learn_skill"])
            results.append((u["username"], score))

    results.sort(key=lambda x: x[1], reverse=True)
    return jsonify(results)


# ---------------- GRAPH ----------------
@app.route("/graph")
def graph():
    matches = {"Best": 0, "Good": 0, "Low": 0}

    data = match().json

    for u in data:
        if u[1] >= 2:
            matches["Best"] += 1
        elif u[1] == 1:
            matches["Good"] += 1
        else:
            matches["Low"] += 1

    return jsonify(matches)


# ---------------- CHAT ----------------
@app.route("/chat/<user>")
def chat(user):
    return render_template("chat.html", other=user)


@app.route("/messages/<user>")
def messages_api(user):
    me = session["user"]
    return jsonify([m for m in messages if (m["sender"], m["receiver"]) in [(me, user), (user, me)]])


@app.route("/send", methods=["POST"])
def send():
    messages.append({
        "sender": session["user"],
        "receiver": request.json["to"],
        "message": request.json["msg"]
    })
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)