import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os

# treat like a secret
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")
print("#######", SIGNING_SECRET)
# =================================#
# Configuration (EDIT IF REQUIRED) #
# =================================#
URL = "https://b12.io/apply/submission"

run_id = os.environ.get("GITHUB_RUN_ID")

payload = {
    "name": "Kevin Lin",
    "email": "kevin.lin.gurudev@outlook.com",
    "resume_link": "https://github.com/fullstack-dev-web/task-for-b12/resume/Kevin_Lin_Resume.pdf",
    "repository_link": "https://github.com/fullstack-dev-web/task-for-b12",
    "action_run_link": f"https://github.com/fullstack-dev-web/task-for-b12/actions/runs/"+ run_id,
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
}

# =========================
# Canonical JSON encoding
# - sorted keys
# - compact separators
# - UTF-8 encoded
# =========================
json_body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")

# =========================
# HMAC-SHA256 signature
# =========================
digest = hmac.new(
    SIGNING_SECRET.encode("utf-8"),
    json_body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={digest}",
}

# =========================
# POST request
# =========================
response = requests.post(URL, data=json_body, headers=headers)
response.raise_for_status()

# =========================
# Print receipt
# =========================
result = response.json()
print(result["receipt"])
