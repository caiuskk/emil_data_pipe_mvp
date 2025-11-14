# api.py
from .client import download_artifact_by_emil
from .parse import bytes_to_dataframe
import pandas as pd


def get_emil_dataset(
    emil_id: str,
    params: dict | None = None,
    file_type: str | None = None,
) -> pd.DataFrame:
    raw = download_artifact_by_emil(emil_id, params=params)
    df = bytes_to_dataframe(raw, file_type=file_type)
    return df


def get_np3_911_er_latest() -> pd.DataFrame:
    # 不指定 file_type，交给 bytes_to_dataframe 自动判断
    return get_emil_dataset("NP3-911-ER")
