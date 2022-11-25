import pandas as pd
import plotly.express as px
import os
import hashlib as hl
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Output, Input
from layout import Layout


# TODO: add callback for name disable tabs, add more sports, make country picker into function and dynamic for different countries

# reads csv to dataframe
df = pd.read_csv("Data/athlete_events.csv")

# psuedo anonymization of names
df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

# makes dataframe of norway
df_norway = df[df["NOC"] == "NOR"]

# func to generate sorted sport dataframe
def sport_picker_df(sport):
    sport_df = df[df["Sport"] == sport]
    sport_df_sorted = (
        sport_df.groupby(["NOC", "Games", "Event", "Medal"])
        .size()
        .reset_index(name="Count")
        .sort_values("Games")
    )

    return sport_df_sorted


# everything to make dash/server work and get layout for page
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = Layout().layout()


@app.callback(
    Output("norway-graph", "figure"),
    Input("graph-picker", "value"),
    Input("adjusted", "value"),
    Input("labels", "n_clicks"),
)
def update_graph_norway(graph, sort, n_clicks):
    # updateds first graph using tab and dropdown

    # tabs used to adjust for teammembers getting same medal
    if sort == "Norway" or graph == "Name":
        df = df_norway
    elif sort == "Norway sorted":
        df = (
            df_norway.groupby(["Games", "Event", "Sport", "Medal"])
            .size()
            .reset_index(name="Count")
        )

    # dropdown to pick what category to plot
    results = (
        df.groupby(graph)["Medal"]
        .count()
        .reset_index(name="Medals_count")
        .sort_values("Medals_count", ascending=False)
    )
    # remove results with 0 medals
    results = results[results["Medals_count"] != 0]

    # generates bar graph of 10 best medalist of category
    fig = px.bar(results.head(10), x=graph, y="Medals_count", template="plotly_dark")
    # updates graph to show or hide xaxis labels based on button press
    fig.update_xaxes(showticklabels=(n_clicks % 2 == 0))

    return fig


@app.callback(
    Output("game-slider", "marks"),
    Output("game-slider", "max"),
    Output("game-slider", "value"),
    Input("sports-picker", "value"),
)
def update_slider(sport):
    # update slider based on sport picked in dropdown

    # updates slidermark by calling func to get sorted dataframe of that sport
    df = sport_picker_df(sport)

    # makes list of all games with that sport then enumerates the list to get markers
    games = df["Games"].unique().tolist()
    marks = {i: mark for i, mark in enumerate(games)}

    # sets max = number of marks
    max = len(marks) - 1
    # sets value of marks to avoid out of range error
    value = 0
    return marks, max, value


@app.callback(
    Output("sports-graph", "figure"),
    Input("sports-picker", "value"),
    Input("game-slider", "value"),
    Input("sport-tabs", "value"),
)
def update_graph_sports(sport, games, tabs):
    # updates seconds graph based on dropdown, tabs and slider

    # gets sorted dataframe of specific sport and makes list of all games for that sport
    sport_df = sport_picker_df(sport)
    all_games = sport_df["Games"].unique().tolist()

    # checks if medal tab or gender tab is selected
    if tabs == "tab-1":
        # picks the specific game to show
        specific_game = sport_df[sport_df["Games"] == all_games[games]]
        # counts number of medals in sport by country in new column
        medal = (
            specific_game.groupby("NOC")["Medal"]
            .count()
            .reset_index(name="Amount")
            .sort_values("Amount", ascending=False)
        )
        # generates pie chart of winners in sport for that years olympics
        fig = px.pie(
            medal,
            names="NOC",
            values="Amount",
            title=f"Medals per country {all_games[games]} olympics",
            template="plotly_dark",
        )
    elif tabs == "tab-2":
        # generates unsorted datafram from specific sport
        sport_df = df[df["Sport"] == sport]
        # picks the specific game to show
        specific_game = sport_df[sport_df["Games"] == all_games[games]]
        # generates pie chart of gender distribution for sport at that years olympics
        fig = px.pie(
            specific_game,
            names="Sex",
            title=f"Gender distribution sailing {all_games[games]} olympics",
            template="plotly_dark",
        )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
