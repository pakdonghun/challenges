
import os
from flask import Flask, render_template, request, send_file, redirect
from scrap import total_datas, save_to_csv_file


os.system("clear")

db = {}

app = Flask("DayThirteen")


@app.route("/")
def home():
    return render_template("final_home.html")


@app.route("/search")
def search():
    word = request.args.get("term")
    word = word.lower()
    if word in db:
        datas = db[word]
    else:
        datas = total_datas(word)
        db[word] = datas
    num = len(datas)
    return render_template("final_search.html", num=num, datas=datas, word=word)


@app.route("/export")
def export():
    try:
        word = request.args.get("term")
        if not word:
            redirect("/")
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        rownames = ["title", "company", "link"]
        save_to_csv_file(jobs, word, rownames)
        return send_file("jobs.csv")
    except:
        return redirect(f"/search?term={word}")

app.run(host="0.0.0.0")
