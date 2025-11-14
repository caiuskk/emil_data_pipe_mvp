# ercot_emil/parse.py
import pandas as pd


def emil_json_to_df(payload: dict) -> pd.DataFrame:
    """
    Parse EMIL JSON report:
    {
      "_meta": {...},
      "report": {...},
      "fields": [...],
      "data": [... or [...]],
      "links": [...]
    }
    """
    data = payload.get("data")
    fields = payload.get("fields") or []

    if not data:
        return pd.DataFrame()

    # array-of-arrays mode
    if isinstance(data, list) and data and isinstance(data[0], list):
        colnames = [f["name"] for f in fields]
        return pd.DataFrame(data, columns=colnames)

    # list-of-dicts mode
    if isinstance(data, list) and isinstance(data[0], dict):
        return pd.DataFrame.from_records(data)

    # fallback
    return pd.DataFrame()
