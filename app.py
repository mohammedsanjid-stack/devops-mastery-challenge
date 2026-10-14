
import os

import pymysql
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "mariadb"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["MARIADB_USER"],
        password=os.environ["MARIADB_PASSWORD"],
        database=os.environ["MARIADB_DATABASE"],
        connect_timeout=3,
        read_timeout=3,
        write_timeout=3,
    )


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Mastery Challenge - Main Branch",
        "status": "running"
    })


@app.route("/api/health")
def health():
    try:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        finally:
            connection.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        app.logger.exception("Database health check failed")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


@app.route("/api/about")
def about():
    return jsonify({
        "project": "DevOps Mastery Challenge",
        "version": "1.0.0",
        "framework": "Flask"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

