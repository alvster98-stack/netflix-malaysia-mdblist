from flask import Flask, jsonify, send_file

app = Flask(__name__)


@app.route("/manifest.json")
def manifest():
    return send_file("manifest.json")


@app.route("/catalog/movie/netflix-malaysia.json")
def movie_catalog():
    return send_file(
        "catalog/movie/netflix-malaysia.json"
    )


@app.route("/catalog/series/netflix-malaysia.json")
def series_catalog():
    return send_file(
        "catalog/series/netflix-malaysia.json"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
