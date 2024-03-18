import pandas as pd
from time import time

data = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/invTypes.csv")
to_exclude = ["groupID", "description","mass","volume","capacity","portionSize","raceID","basePrice","published","marketGroupID","iconID","soundID","graphicID"]
data.drop(labels=to_exclude, inplace=True, axis=1)
data.to_json("data.json", orient="records", index=1)