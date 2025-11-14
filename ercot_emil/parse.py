# parse.py
import io
import zipfile
import pandas as pd


def bytes_to_dataframe(raw: bytes, file_type: str | None = None) -> pd.DataFrame:
    # 简单判断 zip
    if file_type == "zip" or raw[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            # MVP：取第一个文件
            name = zf.namelist()[0]
            with zf.open(name) as f:
                return pd.read_csv(f)
    else:
        # 当作 csv 文本处理
        return pd.read_csv(io.BytesIO(raw))
