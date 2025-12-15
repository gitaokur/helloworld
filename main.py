import os
import json
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_client_ip(req) -> str:
    """
    Cloudflare arkasındayken gerçek IP'yi öncelikle CF-Connecting-IP'ten,
    yoksa X-Forwarded-For'un en soldaki IP'sinden alır.
    """
    cf_ip = req.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip.strip()

    xff = req.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()

    # Fallback: genelde Cloudflare/LB IP'si olur
    return (req.remote_addr or "").strip()

@app.before_request
def log_request():
    payload = {
        "client_ip": get_client_ip(request),
        "method": request.method,
        "path": request.path,
        "user_agent": request.headers.get("User-Agent"),
        "cf_ray": request.headers.get("CF-Ray"),
        "xff": request.headers.get("X-Forwarded-For"),
    }
    logging.info(json.dumps(payload, ensure_ascii=False))

@app.get("/")
def hello():
    return f"Hello World! Your client_ip={get_client_ip(request)}\n", 200

# Geçici debug endpoint (istersen sonradan kaldır)
@app.get("/debug/ip")
def debug_ip():
    return jsonify({
        "client_ip": get_client_ip(request),
        "CF-Connecting-IP": request.headers.get("CF-Connecting-IP"),
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "remote_addr": request.remote_addr,
        "CF-Ray": request.headers.get("CF-Ray"),
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
