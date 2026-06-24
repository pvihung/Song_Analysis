"""
Model tab — placeholder for future ML modelling work.
"""

from dash import html

from dashboard.theme import CARD, COLORS


def layout(df):
    return html.Div(
        style={**CARD, "textAlign": "center", "padding": "60px 40px"},
        children=[
            html.Div(
                style={"fontSize": "48px", "marginBottom": "16px", "opacity": 0.3},
                children="🤖",
            ),
            html.H3("Model — Coming Soon", style={"color": COLORS["text"], "marginTop": 0}),
            html.P(
                "Planned work: train regression / classification models to predict engagement "
                "from audio features, evaluate feature importance, and compare cross-platform performance.",
                style={"color": COLORS["muted"], "maxWidth": "520px", "margin": "0 auto"},
            ),
        ],
    )


def register_callbacks(app, df):
    pass
