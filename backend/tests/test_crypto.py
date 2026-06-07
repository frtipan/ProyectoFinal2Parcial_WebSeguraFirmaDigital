import unittest
import secrets
from backend.crypto.hash_utils import hash_password, verify_password

class TestCrypto(unittest.TestCase):
    def test_hash(self):
        # ✅ Generar un valor aleatorio en cada ejecución
        pwd = secrets.token_hex(8)  # 16 caracteres hex aleatorios
        hashed = hash_password(pwd)

        # ✅ Usar unittest en lugar de assert
        self.assertTrue(verify_password(pwd, hashed))
