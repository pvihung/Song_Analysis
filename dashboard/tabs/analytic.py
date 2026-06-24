"""
Analytic tab — placeholder for future analysis work.
"""

from dash import html

from dashboard.theme import CARD, COLORS


def layout(df):
    return html.Div(
        style={**CARD, "textAlign": "center", "padding": "60px 40px"},
        children=[
            html.Div(
                style={
                    "fontSize": "48px",
                    "marginBottom": "16px",
                    "opacity": 0.3,
                },
                children="📊",
            ),
            html.H3("Analytics — Coming Soon", style={"color": COLORS["text"], "marginTop": 0}),
            html.P(
                "This section will cover deep-dive analyses answering the three research questions:",
                style={"color": COLORS["muted"], "maxWidth": "520px", "margin": "0 auto 20px"},
            ),
            html.Ul(
                style={"textAlign": "left", "maxWidth": "520px", "margin": "0 auto", "color": COLORS["muted"], "lineHeight": "2"},
                children=[
                    html.Li("How do release strategies (album / single / compilation) affect engagement performance?"),
                    html.Li("Do audio feature distributions differ significantly across release formats?"),
                    html.Li("Which audio features correlate most strongly with Spotify Streams and YouTube Views?"),
                ],
            ),
        ],
    )


def register_callbacks(app, df):
    pass
