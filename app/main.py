from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import redis
import os
import time

app = Flask(__name__)

# ── Métriques Prometheus ──
REQUEST_COUNT = Counter(
    'flask_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'HTTP request latency',
    ['endpoint']
)

# ── Connexion Redis ──
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

# ── Middleware : mesure chaque requête ──
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    return response

# ── Routes ──
@app.route("/")
def home():
    try:
        visits = redis_client.incr("visits")
    except:
        visits = 0
    return jsonify({
        "message": "DevOps Platform Complete !",
        "status": "healthy",
        "version": "1.0.0",
        "visits": visits,
        "pod_name": os.getenv("POD_NAME", "local"),
        "node_name": os.getenv("NODE_NAME", "local")
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; charset=utf-8"
    }

@app.route("/api/users")
def users():
    return jsonify({
        "users": ["yosra", "admin", "devops"],
        "count": 3
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)