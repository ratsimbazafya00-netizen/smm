print(">>> LOADER DÉMARRÉ <<<", flush=True)

import json
import time
import hashlib
import os
import sys
import urllib.request
import shutil
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ================= CONFIG =================
GITHUB_USER = "ratsimbazafya00-netizen"
REPO_NAME = "Bot"
BRANCH = "main"

LOADER_VERSION = "1.2.0"
LOCAL_VERSION  = "1.2.0"

# ================= CRYPTO (SEULEMENT KEY) =================
SECRET_B64 = "YTkxZjNjOWUwZjhjMWIyZC4uLg=="

# 🔑 clé AES 32 bytes EXACT (obligatoire)
KEY = hashlib.sha256(base64.b64decode(SECRET_B64)).digest()

# ================= URLS =================
def version_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.json"

def update_file_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/update/smmkingdom.enc"

def license_url(machine_id):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/licenses/{machine_id}.json"

# ================= MACHINE ID =================
def get_machine_id():
    data = os.popen("uname -a").read().strip()
    return hashlib.sha256(data.encode()).hexdigest()

def show_machine_id(mid):
    print("\n" + "=" * 60)
    print("🖥 IDENTIFIANT UNIQUE DE CETTE MACHINE")
    print(mid)
    print("📩 Envoyez cet ID à votre fournisseur")
    print("=" * 60 + "\n")

# ================= REMOTE LOAD =================
def load_remote_version():
    try:
        with urllib.request.urlopen(version_url(), timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

def load_remote_license(mid):
    try:
        with urllib.request.urlopen(license_url(mid), timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

# ================= UPDATE BOT =================
def download_update():
    print("⬇️ Téléchargement mise à jour du bot...")
    try:
        with urllib.request.urlopen(update_file_url(), timeout=30) as r:
            with open("smmkingdom.enc", "wb") as f:
                shutil.copyfileobj(r, f)
        print("✔ Mise à jour bot installée")
        return True
    except Exception as e:
        print("❌ Erreur mise à jour :", e)
        return False

# ================= LICENCE =================
def check_license():
    print("🔍 Vérification licence...")
    mid = get_machine_id()
    lic = load_remote_license(mid)

    if not lic:
        show_machine_id(mid)
        print("❌ Aucune licence trouvée")
        sys.exit(1)

    if lic.get("status") != "active":
        print("❌ Licence désactivée")
        sys.exit(1)

    if time.time() > lic.get("expire", 0):
        print("❌ LICENCE EXPIRÉE")
        sys.exit(1)

    print("✔ LICENCE VALIDE")

# ================= VERSION =================
def check_update():
    print("🔎 Vérification des mises à jour...")
    remote = load_remote_version()

    if not remote:
        print("⚠️ Impossible de vérifier les mises à jour")
        return True

    if remote.get("loader_version") != LOADER_VERSION:
        print("⛔ Mise à jour du loader requise")
        sys.exit(0)

    if remote.get("version") == LOCAL_VERSION:
        print("✔ Version à jour")
        return True

    if remote.get("mandatory"):
        print("⛔ Mise à jour obligatoire")
        return download_update()

    return True

# ================= RUN ENCRYPTED (SANS IV) =================
def run_encrypted():
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import base64, hashlib

    SECRET_B64 = "YTkxZjNjOWUwZjhjMWIyZC4uLg=="
    KEY = hashlib.sha256(base64.b64decode(SECRET_B64)).digest()  # 32 bytes

    with open("smmkingdom.enc", "rb") as f:
        encrypted_b64 = f.read()

    encrypted = base64.b64decode(encrypted_b64)

    cipher = AES.new(KEY, AES.MODE_ECB)

    decrypted = unpad(cipher.decrypt(encrypted), 16)

    code = decrypted.decode("utf-8")

    exec(code, {"__name__": "__main__"})

# ================= MAIN =================
def run():
    check_license()

    if not check_update():
        sys.exit(1)

    if not os.path.exists("smmkingdom.enc"):
        print("⚠️ Bot manquant → téléchargement")
        if not download_update():
            sys.exit(1)

    print("🚀 Lancement SMMKINGDOM...")
    run_encrypted()

if __name__ == "__main__":
    run()

