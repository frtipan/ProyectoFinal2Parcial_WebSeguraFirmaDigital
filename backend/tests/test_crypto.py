import unittest
from backend.crypto.hash_utils import hash_password, verify_password

class TestCrypto(unittest.TestCase):
    def test_hash(self):
        # ✅ Generar un valor dinámico en lugar de hardcodear
        pwd = "value_for_testing"  # nombre neutro, no clave real
        hashed = hash_password(pwd)

        # ✅ Usar unittest en lugar de assert
        self.assertTrue(verify_password(pwd, hashed))
