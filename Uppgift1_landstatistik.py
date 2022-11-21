import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
import hashlib as hl
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Output, Input
from layout import Layout

df = pd.read_csv("Data/athlete_events.csv")

df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

df_norway = df[df["NOC"] == "NOR"]

df_norway_sorted = (
    df_norway.groupby(["Games", "Event", "Sport", "Medal"]).size().reset_index(name="Count")
)

# games_results = (
#     df_norway.groupby("Games")["Medal"]
#     .count()
#     .reset_index(name="Medals_count")
#     .sort_values("Medals_count", ascending=False)
# )

# games_results_adjusted = (
#     df_norway_sorted.groupby("Games")["Medal"]
#     .count()
#     .reset_index(name="Medals_count")
#     .sort_values("Medals_count", ascending=False)
# )

# event_results = (
#     df_norway.groupby("Event")["Medal"]
#     .count()
#     .reset_index(name="Medals_count")
#     .sort_values("Medals_count", ascending=False)
# )

# event_results_adjusted = (
#     df_norway_sorted.groupby("Event")["Medal"]
#     .count()
#     .reset_index(name="Medals_count")
#     .sort_values("Medals_count", ascending=False)
# )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = Layout().layout()


@app.callback(
    Output("norway-graph", "figure"),
    Input("graph-picker", "value"),
    Input("adjusted", "value"),
)
def update_graph(graph, sort):

    if sort == "Norway":
        df = df_norway
    elif sort == "Norway sorted":
        df = df_norway_sorted

    results = (
        df.groupby(graph)["Medal"]
        .count()
        .reset_index(name="Medals_count")
        .sort_values("Medals_count", ascending=False)
    )
    results = results[results["Medals_count"] != 0]

    return px.bar(results.head(10), x=graph, y="Medals_count", template="plotly_dark")


if __name__ == "__main__":
    app.run_server(debug=True)
