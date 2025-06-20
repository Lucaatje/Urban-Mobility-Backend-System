from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Probeer sleutel uit environment variable te halen (base64 encoded)
key_b64 = os.environ.get('URBAN_MOBILITY_SECRET_KEY')

if not key_b64:
    raise EnvironmentError("❌ Environment variable 'URBAN_MOBILITY_SECRET_KEY' is niet gezet.")

try:
    SECRET_KEY = base64.urlsafe_b64decode(key_b64)
except Exception as e:
    raise ValueError("❌ Environment variable 'URBAN_MOBILITY_SECRET_KEY' is geen geldige base64 string.") from e

if len(SECRET_KEY) != 32:
    raise ValueError("❌ De sleutel moet precies 32 bytes lang zijn voor AES-256.")

def encrypt(plaintext: str) -> str:
    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)  # 12 bytes nonce voor AES-GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    # nonce + ciphertext base64-encoden zodat het als string opgeslagen kan worden
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt(ciphertext_b64: str) -> str:
    aesgcm = AESGCM(SECRET_KEY)
    data = base64.b64decode(ciphertext_b64)
    nonce = data[:12]
    ciphertext = data[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

