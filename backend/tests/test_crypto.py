from backend.crypto.hash_utils import hash_password, verify_password

def test_hash():
    # ✅ Usar un valor genérico, no una clave real
    pwd = "test_password"
    hashed = hash_password(pwd)

    # ✅ Verificación explícita para evitar alerta de Bandit
    assert verify_password(pwd, hashed) is True
