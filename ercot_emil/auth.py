# auth.py
import time
import requests
from . import config


_token = None
_token_expire_ts = 0


def get_id_token():
    global _token, _token_expire_ts
    now = time.time()

    # 缓存逻辑：如果 token 还有效，直接返回
    if _token and now < _token_expire_ts:
        return _token

    params = {
        "grant_type": "password",
        "scope": config.SCOPE,
        "client_id": config.CLIENT_ID,
        "username": config.USERNAME,
        "password": config.PASSWORD,
        "response_type": "id_token",
    }

    resp = requests.post(config.TOKEN_URL, data=params)
    resp.raise_for_status()
    data = resp.json()

    _token = data["id_token"]
    _token_expire_ts = now + 55 * 60  # 提前过期

    return _token
