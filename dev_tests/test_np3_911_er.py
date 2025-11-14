# test_np3_911_er.py
from ercot_emil.auth import get_id_token
from ercot_emil import config
import requests
import pandas as pd


def emil_json_to_df(j: dict) -> pd.DataFrame:
    data = j.get("data")
    fields = j.get("fields")

    # 1. If data is empty, return empty DF
    if not data:
        return pd.DataFrame()

    # 2. Check if data is a list of lists (no column names)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        # Get column names
        colnames = [f["name"] for f in fields]
        df = pd.DataFrame(data, columns=colnames)
        return df

    # 3. If it's a list of dicts
    if isinstance(data, list) and isinstance(data[0], dict):
        return pd.DataFrame.from_records(data)

    # 4. Fallback
    return pd.DataFrame()


BASE = "https://api.ercot.com/api/public-reports"


def hit_emil(endpoint: str, **params) -> pd.DataFrame:
    url = f"{BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_id_token()}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
    }
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    j = resp.json()
    print("totalRecords =", j["_meta"]["totalRecords"])
    return emil_json_to_df(j)


df = hit_emil(
    "/np3-911-er/2d_agg_as_offers_ecrsm",
    deliveryDateFrom="2025-01-01",
    deliveryDateTo="2025-01-02",
)

print(df.head())
print(df.dtypes)
