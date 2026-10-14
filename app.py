from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Mastery Challenge",
        "status": "running"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/about")
def about():
    return jsonify({
        "project": "DevOps Mastery Challenge",
        "version": "1.0.0",
        "framework": "Flask"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
