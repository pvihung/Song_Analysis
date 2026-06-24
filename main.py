import warnings
warnings.filterwarnings("ignore")

from dash import Dash, dcc, html, Input, Output

from dashboard.data import load_data
from dashboard.theme import COLORS, tab_style, tab_selected_style
from dashboard.tabs import data_observation, objectives, overview, analytic, model

# ── Data ─────────────────────────────────────────────────────────────────────

df = load_data("sample_data/Spotify_Youtube.csv")

# ── App ───────────────────────────────────────────────────────────────────────

app = Dash(__name__, title="Music Analysis", suppress_callback_exceptions=True)

TABS = [
    ("objectives", "Objectives"),
    ("data-obs",   "Data Observation"),
    ("overview",   "Overview"),
    ("analytic",   "Analytic"),
    ("model",      "Model"),
]

app.layout = html.Div(
    style={"backgroundColor": COLORS["bg_page"], "minHeight": "100vh", "fontFamily": "Inter, sans-serif", "color": COLORS["text"]},
    children=[
        # ── Header ────────────────────────────────────────────────────────────
        html.Div(
            style={
                "background": "linear-gradient(135deg, #1db954 0%, #191414 60%)",
                "padding": "28px 40px",
                "marginBottom": "24px",
            },
            children=[
                html.H1("Music Analysis", style={"margin": 0, "fontSize": "26px", "fontWeight": 700}),
                html.P(
                    "Cross-platform analysis of audio characteristics and audience engagement",
                    style={"margin": "6px 0 0", "opacity": 0.75, "fontSize": "14px"},
                ),
            ],
        ),

        # ── Navigation ────────────────────────────────────────────────────────
        html.Div(style={"padding": "0 32px 32px"}, children=[
            dcc.Tabs(
                id="main-tabs",
                value="objectives",
                style={"marginBottom": "20px"},
                colors={"border": COLORS["bg_subtle"], "primary": COLORS["accent"], "background": COLORS["bg_card"]},
                children=[
                    dcc.Tab(label=label, value=val, style=tab_style(), selected_style=tab_selected_style())
                    for val, label in TABS
                ],
            ),
            html.Div(id="main-tab-content"),
        ]),
    ],
)

# ── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(Output("main-tab-content", "children"), Input("main-tabs", "value"))
def render_tab(tab):
    if tab == "objectives":
        return objectives.layout(df)
    if tab == "data-obs":
        return data_observation.layout(df)
    if tab == "overview":
        return overview.layout(df)
    if tab == "analytic":
        return analytic.layout(df)
    if tab == "model":
        return model.layout(df)


# Register sub-tab callbacks
overview.register_callbacks(app, df)
analytic.register_callbacks(app, df)
model.register_callbacks(app, df)

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=8050)
