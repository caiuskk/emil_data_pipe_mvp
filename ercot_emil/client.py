# client.py
import requests
from . import config
from .auth import get_valid_token


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_valid_token()}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
    }


def get_product(emil_id: str) -> dict:
    url = f"{config.BASE_URL}/public-reports/{emil_id.lower()}"
    resp = requests.get(url, headers=_headers(), timeout=60)
    resp.raise_for_status()
    return resp.json()


def download_artifact(emil_id: str, params: dict | None = None) -> bytes:
    product = get_product(emil_id)
    # MVP 假设 artifacts[0] 就是我们要的
    artifacts = product.get("artifacts") or product.get("_embedded", {}).get(
        "products", []
    )[0].get("artifacts", [])
    endpoint = artifacts[0]["_links"]["endpoint"]["href"]

    resp = requests.get(endpoint, headers=_headers(), params=params, timeout=120)
    resp.raise_for_status()
    return resp.content
