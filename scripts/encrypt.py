"""Wrap the map in a password gate.

The whole map is encrypted with AES-256-GCM; the key is derived from the
password with PBKDF2-HMAC-SHA256 (250,000 iterations). The published file
contains ciphertext only — there is no plaintext copy and no bypass.

    PMA_PASSWORD=yourpassword python3 scripts/encrypt.py
"""
import os, json, base64, hashlib, pathlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = pathlib.Path(__file__).resolve().parent.parent
PW   = os.environ.get("PMA_PASSWORD", "malsyd")
ITER = 250_000

src  = (ROOT / "local/map-unlocked.html").read_bytes()
salt, iv = os.urandom(16), os.urandom(12)
key  = hashlib.pbkdf2_hmac("sha256", PW.encode(), salt, ITER, 32)
ct   = AESGCM(key).encrypt(iv, src, None)
b64  = lambda x: base64.b64encode(x).decode()

gate = (ROOT / "scripts/gate.html").read_text()
gate = gate.replace("__PAYLOAD__", json.dumps(
    {"s": b64(salt), "i": b64(iv), "n": ITER, "c": b64(ct)}, separators=(",", ":")))

out = ROOT / "index.html"
out.write_text(gate)
print(f"{out} — {len(gate)/1048576:.2f} MB — password: {PW}")
