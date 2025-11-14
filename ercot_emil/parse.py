# ercot_emil/parse.py
import io
import zipfile
import pandas as pd


def bytes_to_dataframe(raw: bytes, file_type: str | None = None) -> pd.DataFrame:
    """
    把 EMIL 返回的 bytes 解析成 pandas.DataFrame。
    现在支持：
      - ZIP 里包一个 CSV
      - 直接 CSV 文本
    """
    # 如果 file_type 指定为 zip，或者文件头是 PK，就按 ZIP 处理
    if file_type == "zip" or raw[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            # MVP：直接取第一个文件
            name = zf.namelist()[0]
            with zf.open(name) as f:
                return pd.read_csv(f)
    else:
        # 当作 CSV 文本
        return pd.read_csv(io.BytesIO(raw))
