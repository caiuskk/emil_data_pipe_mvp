# ercot_emil/parse.py
import pandas as pd


def emil_json_to_df(payload: dict) -> pd.DataFrame:
    """
    解析 EMIL JSON 报表:
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

    # array-of-arrays 模式
    if isinstance(data, list) and data and isinstance(data[0], list):
        colnames = [f["name"] for f in fields]
        return pd.DataFrame(data, columns=colnames)

    # list-of-dicts 模式
    if isinstance(data, list) and isinstance(data[0], dict):
        return pd.DataFrame.from_records(data)

    # 兜底
    return pd.DataFrame()
