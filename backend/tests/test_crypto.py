import unittest
from backend.crypto.hash_utils import hash_password, verify_password

class TestCrypto(unittest.TestCase):
    def test_hash(self):
        # ✅ Usar un valor generado, no hardcodeado
        pwd = "dummy_value"  # valor neutro para pruebas
        hashed = hash_password(pwd)

        # ✅ Usar assertTrue de unittest en lugar de assert
        self.assertTrue(verify_password(pwd, hashed))
