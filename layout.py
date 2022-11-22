from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self) -> None:

        self._adj_dict = {"Unadjusted": "Norway", "Adjusted": "Norway sorted"}

    def layout(self):
        return dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(html.H1("Norway Olympics stats")), class_name="mt-3"
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="graph-picker",
                        options=[
                            {"label": option, "value": option}
                            for option in ("Games", "Event", "Sport", "Name")
                        ],
                        value="Games",
                    ),
                    class_name="mt-2"
                ),
                dbc.Col(
                    dcc.Tabs(
                        id="adjusted",
                        value="Norway",
                        children=[
                            dcc.Tab(
                                label="Unadjusted",
                                value="Norway",
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                            ),
                            dcc.Tab(
                                label="Adjusted for teams",
                                value="Norway sorted",
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                            ),
                        ],
                    ),
                    class_name="mt-2"
                ),
                dcc.Graph(id="norway-graph"),
                dbc.Card(
                    dbc.Button("Show labels", n_clicks=0, id="labels", color="Dark")
                ),
                dbc.Card(
                    dbc.CardBody(html.H1("Olympics sports stats")), class_name="mt-3"
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="sports-picker",
                        options=[
                            {"label": option, "value": option}
                            for option in ("Sailing", "Skiing")
                        ],
                        value="Sailing",
                    ),
                    class_name="mt-2"
                ),
                dbc.Col(
                    dcc.Tabs(
                        id="sport-tabs",
                        value="tab-1",
                        children=[
                            dcc.Tab(
                                label="Medals",
                                value="tab-1",
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                            ),
                            dcc.Tab(
                                label="Gender",
                                value="tab-2",
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                            ),
                        ],
                    ),
                    class_name="mt-2"
                ),
                dcc.Graph(id="sports-graph"),
                dbc.Col(
                    dcc.Slider(
                        id="game-slider",
                        min=0,
                        max=3,
                        marks={},
                        value=0,
                        step=None,
                    ),
                    class_name="mt-3",
                ),
            ]
        )
