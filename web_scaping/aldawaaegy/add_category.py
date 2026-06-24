import pandas as pd

df = pd.read_csv("aldawaa_products.csv")

df["Category"] = "aldawaa_products"

df.to_csv("aldawaa_products.csv", index=False)