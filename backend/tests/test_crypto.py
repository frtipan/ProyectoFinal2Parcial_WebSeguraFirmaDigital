from crypto.hash_utils import hash_password, verify_password

def test_hash():
    pwd = "seguro123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
