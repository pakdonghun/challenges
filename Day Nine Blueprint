import requests
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


def get_lists(url):
    lists = []
    results = requests.get(url)
    result = results.json()
    hits = result.get("hits")

    for hit in hits:
        lists.append(hit)

    return lists


db = {}
app = Flask("DayNine")


@app.route("/")
def home():
    order = request.args.get('order_by', 'popular')
    print(order)

    if order == "new":

        existingList = db.get(order)

        if existingList:
            lists = existingList

        else:
            lists = get_lists(new)
            db[order] = lists

        return render_template("index.html", order=order, lists=lists)

    elif order == "popular":

        existingList = db.get(order)

        if existingList:
            lists = existingList

        else:
            lists = get_lists(popular)
            db[order] = lists

        return render_template("index.html", order=order, lists=lists)

    else:
        return redirect("/")


@app.route("/<id>")
def detail(id):
    print(id)
    url = make_detail_url(id)
    results = requests.get(url)
    result = results.json()
    comments = result["children"]

    return render_template("detail.html", result=result, comments=comments)


app.run(host="0.0.0.0")
