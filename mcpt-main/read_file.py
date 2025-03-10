import pandas as pd

df = pd.read_parquet("trading_data.pq")
print(df.head())  # Show first 5 rows

print(len(df))