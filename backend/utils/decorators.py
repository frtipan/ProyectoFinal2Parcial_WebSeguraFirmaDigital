from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity.get("rol") != "admin":
            return jsonify({"error": "Acceso solo para administradores"}), 403
        return fn(*args, **kwargs)
    return wrapper
