from flask import Flask, jsonify
import json

app = Flask(__name__)


@app.route("/manifest.json")
def manifest():
    with open("manifest.json") as f:
        return jsonify(json.load(f))


@app.route("/catalog/<type>/<id>.json")
def catalog(type, id):

    if type == "movie":
        file = "catalog/movie/netflix-malaysia.json"

    else:
        file = "catalog/series/netflix-malaysia.json"

    with open(file) as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
