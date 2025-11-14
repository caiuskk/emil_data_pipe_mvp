import time
import requests
from . import config

_token = None
_token_expire_ts = 0


def get_id_token(dbg=False) -> str:
    global _token, _token_expire_ts
    now = time.time()

    if _token and now < _token_expire_ts:
        return _token

    payload = {
        "grant_type": "password",
        "scope": config.SCOPE,
        "client_id": config.CLIENT_ID,
        "username": config.USERNAME,
        "password": config.PASSWORD,
        "response_type": "id_token",
    }
    if dbg:
        print("DEBUG – going to request token with:")
        print("  TOKEN_URL:", config.TOKEN_URL)
        print("  USERNAME:", config.USERNAME)
        print("  SCOPE:", config.SCOPE)
        print("  CLIENT_ID:", config.CLIENT_ID)

    resp = requests.post(
        config.TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if dbg:
        print("DEBUG – status:", resp.status_code)
        print("DEBUG – raw response text:")
        print(resp.text[:1000])  # Only look at the first 1000 chars

    resp.raise_for_status()
    data = resp.json()

    _token = data["id_token"]
    _token_expire_ts = now + 55 * 60
    return _token
