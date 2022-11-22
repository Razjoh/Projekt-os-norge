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

df_sailing = df[df["Sport"] == "Sailing"]
df_sailing_sorted = df_sailing.groupby(["NOC", "Games", "Event", "Medal"]).size().reset_index(name="Count").sort_values("Games")
games_sailing = df_sailing_sorted["Games"].unique().tolist()

df_skiing = df[df["Sport"] == "Cross Country Skiing"]
df_skiing_sorted = df_skiing.groupby(["NOC", "Games", "Event", "Medal"]).size().reset_index(name="Count").sort_values("Games")
games_skiing = df_skiing_sorted["Games"].unique().tolist()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

server = app.server

app.layout = Layout().layout()


@app.callback(
    Output("norway-graph", "figure"),
    Input("graph-picker", "value"),
    Input("adjusted", "value"),
    Input("labels", "n_clicks")
)
def update_graph_norway(graph, sort, n_clicks):

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

    fig = px.bar(results.head(10), x=graph, y="Medals_count", template="plotly_dark")

    fig.update_xaxes(showticklabels=(n_clicks%2==0))

    return fig

@app.callback(
    Output("game-slider", "marks"),
    Output("game-slider", "max"),
    Input("sports-picker", "value")
)
def update_slider(sport):
    if sport == "Sailing":
        marks = {i: mark for i, mark in enumerate(games_sailing)}
    elif sport == "Skiing":
        marks = {i: mark for i, mark in enumerate(games_skiing)}

    max = len(marks) -1
    return marks, max

@app.callback(
    Output("sports-graph", "figure"),
    Input("sports-picker", "value"),
    Input("game-slider", "value"),
    Input("sport-tabs", "value")
)
def update_graph_sports(sport, games, tabs):

    if sport == "Sailing":
        if tabs == "tab-1":
            specific_game = df_sailing_sorted[df_sailing_sorted["Games"] == games_sailing[games]]
            medal = specific_game.groupby("NOC")["Medal"].count().reset_index(name="Amount").sort_values("Amount",ascending=False)
            fig = px.pie(medal, names="NOC", values="Amount", title=f"Medals per country {games_sailing[games]} olympics", template="plotly_dark")
        elif tabs == "tab-2":
            fig = px.pie(df_sailing[df_sailing["Games"] == games_sailing[games]], names="Sex", title=f"Gender distribution sailing {games_sailing[games]} olympics", template="plotly_dark")

    elif sport == "Skiing":
        if tabs == "tab-1":
            specific_game = df_skiing_sorted[df_skiing_sorted["Games"] == games_skiing[games]]
            medal = specific_game.groupby("NOC")["Medal"].count().reset_index(name="Amount").sort_values("Amount",ascending=False)
            fig = px.pie(medal, names="NOC", values="Amount", title=f"Medals per country {games_skiing[games]} olympics", template="plotly_dark")
        elif tabs == "tab-2":
            fig = px.pie(df_skiing[df_skiing["Games"] == games_skiing[games]], names="Sex", title=f"Gender distribution cross country skiing {games_skiing[games]} olympics", template="plotly_dark")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
