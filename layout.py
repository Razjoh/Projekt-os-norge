from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self) -> None:

        self._adj_dict = {"Unadjusted": "Norway", "Adjusted": "Norway sorted"}

    def layout(self):
        return dbc.Container(
                [
                    dbc.Card(dbc.CardBody(html.H1("Norway Olympics stats")), class_name="mt-3"),
                    
                    dbc.Row(class_name="mt-3",
                    children=[
                        dbc.Col(html.P("Pick a graph")),

                        dbc.Col(dcc.Dropdown(
                            id="graph-picker",
                            options=[
                                {"label": option, "value": option}
                                for option in ("Games", "Event", "Sport", "Name")
                                ],
                            value="Games",
                            )),

                        dbc.Col(dcc.RadioItems(
                            id="adjusted",
                            options=[
                                {"label": option, "value": name}
                                for option, name in self._adj_dict.items()
                                ],
                            value="Norway",
                            inline=False
                            )),

                        ]),
                    
                    dcc.Graph(id="norway-graph"),
                    dbc.Card(dbc.Button("Show labels", n_clicks=0, id="labels", color="Dark"))
                ]
        )
