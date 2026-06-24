"""
Overview tab — distributions, correlation heatmaps, cross-platform scatter,
release strategy breakdown, top artists & tracks.
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, Input, Output

from dashboard.data import AUDIO_FEATURES, ENGAGEMENT, ALBUM_COLORS
from dashboard.theme import CARD, COLORS, dark_layout


# ── Sub-section builders ─────────────────────────────────────────────────────

def _distributions(df):
    fig_audio = make_subplots(rows=3, cols=3, subplot_titles=AUDIO_FEATURES)
    for i, feat in enumerate(AUDIO_FEATURES):
        r, c = divmod(i, 3)
        fig_audio.add_trace(
            go.Histogram(x=df[feat], nbinsx=40, marker_color=COLORS["accent"], opacity=0.75, showlegend=False),
            row=r + 1, col=c + 1,
        )
    fig_audio.update_layout(**dark_layout("Audio Feature Distributions", height=680))

    fig_eng = make_subplots(rows=1, cols=4, subplot_titles=ENGAGEMENT)
    for i, col in enumerate(ENGAGEMENT):
        fig_eng.add_trace(
            go.Histogram(x=np.log1p(df[col].dropna()), nbinsx=40, marker_color="#EF553B", opacity=0.75, showlegend=False),
            row=1, col=i + 1,
        )
    fig_eng.update_layout(**dark_layout("Engagement Metrics — log(1 + x) scale", height=300))

    return html.Div([
        html.Div(style=CARD, children=[dcc.Graph(figure=fig_audio)]),
        html.Div(style=CARD, children=[dcc.Graph(figure=fig_eng)]),
    ])


def _correlations(df):
    spotify_cols = AUDIO_FEATURES + ["Stream"]
    yt_cols = AUDIO_FEATURES + ["Views", "Likes", "Comments"]

    fig_sp = px.imshow(
        df[spotify_cols].dropna().corr(), text_auto=".2f",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Spotify — Audio Features × Streams",
    )
    fig_sp.update_layout(**dark_layout(height=520))

    fig_yt = px.imshow(
        df[yt_cols].dropna().corr(), text_auto=".2f",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="YouTube — Audio Features × Views / Likes / Comments",
    )
    fig_yt.update_layout(**dark_layout(height=560))

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_sp)]),
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_yt)]),
            ],
        ),
    ])


def _release_strategy(df):
    melt = df[["Album_type"] + ["Stream", "Views"]].melt(id_vars="Album_type", var_name="Metric", value_name="Value")
    melt["log_Value"] = np.log1p(melt["Value"])

    fig_box = px.box(
        melt, x="Album_type", y="log_Value", color="Metric",
        title="Streams & Views by Release Type (log scale)",
        color_discrete_sequence=[COLORS["accent"], "#EF553B"],
        category_orders={"Album_type": ["album", "single", "compilation"]},
    )
    fig_box.update_layout(**dark_layout(height=440))

    # Radar: avg audio profile per release type (normalised)
    radar_data = df.groupby("Album_type", observed=True)[AUDIO_FEATURES].mean().reset_index()
    radar_norm = radar_data.copy()
    for f in AUDIO_FEATURES:
        mn, mx = df[f].min(), df[f].max()
        radar_norm[f] = (radar_norm[f] - mn) / (mx - mn + 1e-9)

    fig_radar = go.Figure()
    palette = [COLORS["accent"], "#EF553B", "#ab63fa"]
    for idx, row in radar_norm.iterrows():
        vals = [row[f] for f in AUDIO_FEATURES]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=AUDIO_FEATURES + [AUDIO_FEATURES[0]],
            fill="toself",
            name=str(row["Album_type"]),
            line_color=palette[idx % len(palette)],
            opacity=0.65,
        ))
    fig_radar.update_layout(
        **dark_layout("Avg Audio Profile by Release Type (normalised)", height=480),
        polar={"bgcolor": COLORS["bg_card"], "radialaxis": {"color": "#555"}},
    )

    counts = df["Album_type"].value_counts().reset_index()
    counts.columns = ["Album_type", "count"]
    fig_pie = px.pie(counts, names="Album_type", values="count", color="Album_type",
                     color_discrete_map=ALBUM_COLORS, title="Track Count by Release Type")
    fig_pie.update_layout(**dark_layout(height=360))

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "20px"},
            children=[
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_box)]),
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_pie)]),
            ],
        ),
        html.Div(style=CARD, children=[dcc.Graph(figure=fig_radar)]),
    ])


def _cross_platform(df):
    tmp = df[["Track", "Artist", "Album_type", "Stream", "Views", "Danceability"]].dropna()
    tmp = tmp.copy()
    tmp["log_Stream"] = np.log1p(tmp["Stream"])
    tmp["log_Views"] = np.log1p(tmp["Views"])

    fig = px.scatter(
        tmp, x="log_Stream", y="log_Views",
        color="Album_type", color_discrete_map=ALBUM_COLORS,
        size="Danceability", size_max=12,
        trendline="ols",
        hover_data={"Artist": True, "Track": True, "Stream": True, "Views": True,
                    "log_Stream": False, "log_Views": False},
        title="Spotify Streams vs YouTube Views — size = Danceability",
        labels={"log_Stream": "log(1 + Streams)", "log_Views": "log(1 + Views)"},
        opacity=0.45,
    )
    fig.update_layout(**dark_layout(height=520))
    return html.Div(style=CARD, children=[dcc.Graph(figure=fig)])


def _top_artists_tracks(df):
    from dashboard.data import artist_aggregates
    artist_df = artist_aggregates(df).head(20)

    fig_artists = px.bar(
        artist_df, x="Total_Streams", y="Artist", orientation="h",
        color="Total_Streams", color_continuous_scale="Greens",
        title="Top 20 Artists by Total Spotify Streams", text_auto=".2s",
    )
    fig_artists.update_layout(**dark_layout(height=540))
    fig_artists.update_yaxes(autorange="reversed")

    top_tracks = (
        df[["Track", "Artist", "Album_type", "Stream", "Danceability", "Energy", "Valence"]]
        .dropna(subset=["Stream"])
        .sort_values("Stream", ascending=False)
        .head(20)
        .round(3)
    )
    fig_tracks = px.bar(
        top_tracks, x="Stream", y="Track", orientation="h",
        color="Danceability", color_continuous_scale="Tealgrn",
        title="Top 20 Tracks by Streams — color = Danceability", text_auto=".2s",
    )
    fig_tracks.update_layout(**dark_layout(height=540))
    fig_tracks.update_yaxes(autorange="reversed")

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_artists)]),
                html.Div(style=CARD, children=[dcc.Graph(figure=fig_tracks)]),
            ],
        ),
    ])


# ── Section tabs inside Overview ─────────────────────────────────────────────

SECTIONS = [
    ("dist", "Distributions"),
    ("corr", "Correlations"),
    ("release", "Release Strategy"),
    ("cross", "Cross-Platform"),
    ("artists", "Top Artists & Tracks"),
]

_SECTION_TAB_STYLE = {
    "backgroundColor": "#252535",
    "color": COLORS["muted"],
    "border": f"1px solid {COLORS['bg_subtle']}",
    "padding": "8px 16px",
    "borderRadius": "4px 4px 0 0",
    "fontSize": "13px",
}
_SECTION_TAB_SELECTED = {
    **_SECTION_TAB_STYLE,
    "backgroundColor": COLORS["bg_subtle"],
    "color": COLORS["accent"],
    "borderBottom": f"2px solid {COLORS['accent']}",
}


def layout(df):
    return html.Div([
        dcc.Tabs(
            id="overview-section",
            value="dist",
            style={"marginBottom": "16px"},
            colors={"border": COLORS["bg_subtle"], "primary": COLORS["accent"], "background": COLORS["bg_card"]},
            children=[
                dcc.Tab(label=label, value=val, style=_SECTION_TAB_STYLE, selected_style=_SECTION_TAB_SELECTED)
                for val, label in SECTIONS
            ],
        ),
        html.Div(id="overview-section-content"),
    ])


def register_callbacks(app, df):
    @app.callback(
        Output("overview-section-content", "children"),
        Input("overview-section", "value"),
    )
    def render_section(section):
        if section == "dist":
            return _distributions(df)
        if section == "corr":
            return _correlations(df)
        if section == "release":
            return _release_strategy(df)
        if section == "cross":
            return _cross_platform(df)
        if section == "artists":
            return _top_artists_tracks(df)
