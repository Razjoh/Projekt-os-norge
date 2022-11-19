import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
import hashlib as hl

df = pd.read_csv("Data/athlete_events.csv")

df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
df_norway = df[df["NOC"] == "NOR"]

df_norway_sorted = (
    df_norway.groupby(["Games", "Event", "Medal"]).size().reset_index(name="Count")
)

games_results = (
    df_norway.groupby("Games")["Medal"]
    .count()
    .reset_index(name="Medals_count")
    .sort_values("Medals_count", ascending=False)
)

games_results_adjusted = (
    df_norway_sorted.groupby("Games")["Medal"]
    .count()
    .reset_index(name="Medals_count")
    .sort_values("Medals_count", ascending=False)
)

event_results = (
    df_norway.groupby("Event")["Medal"]
    .count()
    .reset_index(name="Medals_count")
    .sort_values("Medals_count", ascending=False)
)

event_results_adjusted = (
    df_norway_sorted.groupby("Event")["Medal"]
    .count()
    .reset_index(name="Medals_count")
    .sort_values("Medals_count", ascending=False)
)


fig = px.bar(games_results_adjusted, x="Games", y="Medals_count")
fig.show()
#print(df_norway.head())
