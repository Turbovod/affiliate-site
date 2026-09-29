import os, base64, json, subprocess, sys
import requests
from nacl import encoding, public

# Configuration - replace with your own values or set via env vars
def main():
    repo = "Turbovod/affiliate-site"
    token = os.getenv("GITHUB_PAT")
    if not token:
        print("Error: GITHUB_PAT environment variable not set")
        sys.exit(1)
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    # 1. Get the public key for encrypting secrets
    pubkey_url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    resp = requests.get(pubkey_url, headers=headers)
    resp.raise_for_status()
    pubkey_data = resp.json()
    key_id = pubkey_data["key_id"]
    key = pubkey_data["key"]
    public_key = public.SealedBox(public.PublicKey(key.encode(), encoding.Base64Encoder()))
    # Secrets to add
    secrets = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    }
    for name, value in secrets.items():
        if not value:
            print(f"Skipping secret {name}: no value in environment")
            continue
        encrypted = public_key.encrypt(value.encode())
        encrypted_b64 = base64.b64encode(encrypted).decode()
        secret_url = f"https://api.github.com/repos/{repo}/actions/secrets/{name}"
        payload = {"encrypted_value": encrypted_b64, "key_id": key_id}
        r = requests.put(secret_url, headers=headers, json=payload)
        if r.status_code in (201, 204):
            print(f"Secret {name} set successfully")
        else:
            print(f"Failed to set secret {name}: {r.status_code} {r.text}")
    # 2. Enable GitHub Pages (source: gh-pages branch)
    pages_url = f"https://api.github.com/repos/{repo}/pages"
    pages_payload = {"source": {"branch": "gh-pages", "path": "/"}}
    r = requests.post(pages_url, headers=headers, json=pages_payload)
    if r.status_code in (201, 202):
        print("GitHub Pages enabled successfully")
    else:
        print(f"Failed to enable GitHub Pages: {r.status_code} {r.text}")

if __name__ == "__main__":
    main()
