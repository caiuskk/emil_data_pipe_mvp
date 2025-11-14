# ercot_emil/client.py
import requests
from .auth import get_id_token
from . import config


def _headers() -> dict:
    """公共请求头：Bearer token + subscription key。"""
    return {
        "Authorization": f"Bearer {get_id_token()}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
    }


def get_product(emil_id: str) -> dict:
    """拉某个 EMIL 报表的 metadata（里面有 artifacts / endpoint）。"""
    url = f"{config.BASE_URL}/public-reports/{emil_id.lower()}"
    resp = requests.get(url, headers=_headers(), timeout=60)
    resp.raise_for_status()
    return resp.json()


def get_artifact_endpoint(product_json: dict, index: int = 0) -> str:
    """
    从产品 JSON 里找到下载地址 endpoint。
    一般 artifacts[0] 就是我们要的。
    """
    artifacts = product_json.get("artifacts")
    if not artifacts:
        embedded = product_json.get("_embedded", {})
        products = embedded.get("products", [])
        if products:
            artifacts = products[0].get("artifacts")

    if not artifacts:
        raise ValueError("No artifacts found in product JSON")

    return artifacts[index]["_links"]["endpoint"]["href"]


def download_artifact_by_emil(
    emil_id: str,
    params: dict | None = None,
    artifact_index: int = 0,
) -> bytes:
    """
    给一个 emil_id（比如 NP3-911-ER），返回原始文件的 bytes。
    params 暂时可以先 None（拿最新一次）。
    """
    product = get_product(emil_id)
    endpoint = get_artifact_endpoint(product, artifact_index)
    resp = requests.get(endpoint, headers=_headers(), params=params, timeout=120)
    resp.raise_for_status()
    return resp.content
