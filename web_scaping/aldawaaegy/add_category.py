import pandas as pd

df = pd.read_csv("2025-offers.csv")

df["Category"] = "offers"

df.to_csv("2025-offers.csv", index=False)