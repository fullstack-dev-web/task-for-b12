import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

# =================================#
# Configuration (EDIT IF REQUIRED) #
# =================================#
URL = "https://b12.io/apply/submission"
SIGNING_SECRET = b"hello-there-from-b12"  # treat like a secret

payload = {
    "name": "Kevin Lin",
    "email": "kevin.lin.gurudev@outlook.com",
    "resume_link": "https://github.com/fullstack-dev-web/task-for-b12/resume/Kevin_Lin_Resume.pdf",
    "repository_link": "https://github.com/fullstack-dev-web/task-for-b12",
    "action_run_link": "https://github.com/fullstack-dev-web/task-for-b12/actions/runs",
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
    SIGNING_SECRET,
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
