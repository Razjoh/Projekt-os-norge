from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    """"class to generate layout for dash page """
    
    def __init__(self) -> None:

        self._adj_dict = {"Unadjusted": "Norway", "Adjusted": "Norway sorted"}

    def layout(self):
        return dbc.Container(
            [
                # First header: Norway
                dbc.Card(
                    dbc.CardBody(html.H1("Norway Olympics stats")), class_name="mt-3"
                ),
                dbc.Col(
                    # Dropdown filter picker first graph 
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
                    # Tabs to pick adjusting for teams first graph
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
                # First graph: stats Norway
                dcc.Graph(id="norway-graph"),
                # Hide show graph x labels
                dbc.Card(
                    dbc.Button("Show labels", n_clicks=0, id="labels", color="Dark")
                ),
                # Second header: Sports
                dbc.Card(
                    dbc.CardBody(html.H1("Olympics sports stats")), class_name="mt-3"
                ),
                dbc.Col(
                    # Dropdown filter pick sport second graph
                    dcc.Dropdown(
                        id="sports-picker",
                        options=[
                            {"label": option, "value": option}
                            for option in ("Sailing", "Cross Country Skiing")
                        ],
                        value="Sailing",
                    ),
                    class_name="mt-2"
                ),
                dbc.Col(
                    # Tabs to pick filter medals or gender second graph
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
                # Second graph sports medals/gender every olympics
                dcc.Graph(id="sports-graph"),
                dbc.Col(
                    # slider to pick olympics to show
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
