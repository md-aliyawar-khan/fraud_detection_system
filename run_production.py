import os

from waitress import serve

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Use a production-grade WSGI server for realistic load measurements.
    serve(app, host="0.0.0.0", port=port, threads=8)
