# ercot_emil/client.py
from __future__ import annotations

import requests
import pandas as pd
from typing import Any, Dict, Optional

from .auth import get_id_token
from . import config
from .parse import emil_json_to_df


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_id_token()}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
    }


def get_report_json(
    path: str, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Call the JSON report endpoint.
    Path looks like: "/public-reports/np3-911-er/2d_agg_as_offers_ecrsm"
    """
    url = f"{config.BASE_URL}{path}"  # BASE_URL = "https://api.ercot.com/api"
    resp = requests.get(url, headers=_headers(), params=params or {}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def get_report_df(path: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Return a DataFrame directly.
    """
    payload = get_report_json(path, params=params)
    return emil_json_to_df(payload)
