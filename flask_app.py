from flask import Flask, render_template, request, redirect, url_for, session
import main

app = Flask(__name__)
app.static_folder="static"

app.secret_key = "some secret key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["uri"] = main.url_to_uri(request.form["uri"])
        session["name"] = request.form["username"]
        return redirect(url_for("playlist"))
    return render_template("index.html", current_url="/")

@app.route("/about")
def about():
    return render_template("about.html", current_url="/about")

@app.route("/playlist")
def playlist():
    uri = session.get("uri", None)
    name = session.get("name", None)
    full_uri = f"spotify:playlist:{name}:{uri}"
    #full_uri = "spotify:playlist:{}:{}".format(name, uri)
    pl = main.main(full_uri)
    session["full_uri"] = full_uri
    session["pl"] = pl
    if pl == None:
        return render_template("no-playlist.html")
    if pl == "Connection Error":
        return render_template("bad-connection.html")

    return render_template("playlist.html", name=name, playlist=pl)

@app.route("/playlist-table")
def playlisttable():
    name = session.get("name", None)
    uri = session.get("full_uri", None)
    pl = session.get("pl", None)
    if uri == None:
        return render_template("no-playlist.html")

    return render_template("playlist-table.html", name=name, playlist=pl)

@app.route("/profile-url-conversion", methods=["GET", "POST"])
def profileconvert():
    username = None
    if request.method == "POST":
        userurl = request.form["userurl"]
        username = main.profileurl(userurl)
    return render_template("profile.html", username=username, current_url="/profile-url-conversion")

if __name__ == "__main__":
    app.run(debug=True, port=80)