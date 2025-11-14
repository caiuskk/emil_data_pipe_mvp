# api.py
from datetime import date
import pandas as pd
from .client import download_artifact
from .parse import bytes_to_dataframe


def get_emil_dataset(
    emil_id: str,
    for_date: date | None = None,
    file_type: str | None = None,
    extra_params: dict | None = None,
) -> pd.DataFrame:
    params = {}
    if extra_params:
        params.update(extra_params)

    if for_date:
        # 这里具体用啥 param，视报表而定，MVP 可以先硬编码一两种
        params["operatingDate"] = for_date.strftime("%Y-%m-%d")

    raw = download_artifact(emil_id, params=params)
    df = bytes_to_dataframe(raw, file_type=file_type)
    return df
