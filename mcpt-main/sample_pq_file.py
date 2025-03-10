import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Define the total number of required data points
num_data_points = 36000

# Generate a date range with hourly frequency to get exactly 35040 timestamps
date_range = pd.date_range(start="2015-01-01", periods=num_data_points, freq="H")  # Hourly data

# Generate random OHLC trading data
open_prices = np.random.uniform(100, 200, num_data_points)
high_prices = open_prices + np.random.uniform(0, 10, num_data_points)
low_prices = open_prices - np.random.uniform(0, 10, num_data_points)
close_prices = np.random.uniform(low_prices, high_prices)
volumes = np.random.randint(1000, 10000, num_data_points)

# Create a DataFrame
df = pd.DataFrame({
    "date": date_range,
    "open": open_prices,
    "high": high_prices,
    "low": low_prices,
    "close": close_prices,
    "volume": volumes,
})

# Set the Date column as the index
df.set_index("date", inplace=True)

# Save as a Parquet file
file_path = "/home/gopika/Documents/mcpt-main/trading_data.pq"
df.to_parquet(file_path, engine="pyarrow")  # Use "fastparquet" if needed

print(f"Trading Parquet file saved as '{file_path}' with {len(df)} records!")
