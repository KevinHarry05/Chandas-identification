import json
import pandas as pd

with open("data/examples.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["examples"])

print("Columns:", df.columns)
print(df.head())
