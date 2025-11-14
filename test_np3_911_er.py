# test_np3_911_er.py
from ercot_emil.api import get_np3_911_er_latest

df = get_np3_911_er_latest()

print("Columns:", df.columns.tolist())
print("Head:")
print(df.head())
print("Row count:", len(df))
