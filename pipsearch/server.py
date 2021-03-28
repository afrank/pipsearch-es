
from pipsearch.util.search import setup_es, search, refresh_pkg_metadata

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def main():
    """
    here lies the flask app for serving up elasticsearch results.
    """
    q = request.args.get("q", "")
    if not q:
        return jsonify({ "error": "Must provide something to search for!"})
    
    es = setup_es()

    result = search(es, q)

    max_score = max([ x["_score"] for x in result ])
    min_score = max_score * 0.75 # show only top 25% of search results

    out = []

    for r in result:
        score = r["_score"]
        latest = r["_source"]["latest_version"].strip()
        summary = r["_source"]["summary"].strip()
        name = r["_source"]["name"].strip()

        if score < min_score:
            continue

        res = { "name": name,
                "summary": summary,
                "latest": latest,
                "score": score
        }

        out += [res]
    return jsonify(out)

if __name__ == '__main__':
    app.run()
