from dash import html
from dashboard.theme import COLORS, CARD

_ACCENT = COLORS["accent"]
_BLUE = "#1da1f2"
_PURPLE = "#9b59b6"

# ── helpers ──────────────────────────────────────────────────────────────────

def _section_title(text: str) -> html.H3:
    return html.H3(text, style={
        "color": COLORS["text"],
        "fontSize": "17px",
        "fontWeight": 700,
        "margin": "28px 0 14px",
        "borderBottom": f"1px solid {COLORS['bg_subtle']}",
        "paddingBottom": "8px",
    })


def _sub_title(text: str) -> html.H4:
    return html.H4(text, style={
        "color": COLORS["muted"],
        "fontSize": "13px",
        "fontWeight": 600,
        "fontStyle": "italic",
        "margin": "20px 0 10px",
        "letterSpacing": "0.03em",
    })


def _numbered_question(num: int, text: str, color: str) -> html.Div:
    return html.Div(
        style={"display": "flex", "gap": "14px", "alignItems": "flex-start", "marginBottom": "14px"},
        children=[
            html.Div(
                str(num),
                style={
                    "backgroundColor": color,
                    "color": "#fff",
                    "fontWeight": 700,
                    "fontSize": "13px",
                    "borderRadius": "50%",
                    "width": "26px",
                    "height": "26px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "flexShrink": 0,
                    "marginTop": "1px",
                },
            ),
            html.P(text, style={"margin": 0, "color": COLORS["muted"], "lineHeight": "1.75", "fontSize": "14px"}),
        ],
    )


def _dataset_badge(label: str, items: str, color: str) -> html.Div:
    return html.Div(
        style={
            **CARD,
            "borderLeft": f"4px solid {color}",
            "marginBottom": "12px",
            "padding": "14px 18px",
        },
        children=[
            html.Span(label, style={"fontWeight": 700, "color": color, "fontSize": "14px"}),
            html.Span(f": {items}", style={"color": COLORS["muted"], "fontSize": "14px"}),
        ],
    )


# ── layout ────────────────────────────────────────────────────────────────────

def layout(_df=None) -> html.Div:
    return html.Div([

        # ── Project Overview ─────────────────────────────────────────────────
        html.Div(
            style={**CARD, "borderLeft": f"4px solid {_ACCENT}"},
            children=[
                html.H2("Project Overview", style={"margin": "0 0 12px", "color": _ACCENT, "fontSize": "20px", "fontWeight": 700}),
                html.P(
                    [
                        "This project focuses on a comprehensive cross-platform analysis of music tracks "
                        "using data combined from ",
                        html.Strong("Spotify", style={"color": _ACCENT}),
                        " and ",
                        html.Strong("YouTube", style={"color": "#ff0000"}),
                        ". The core objective is to uncover relationships between ",
                        html.Strong("audio characteristics"),
                        " (e.g., how danceable, energetic, or long a song is) and ",
                        html.Strong("audience engagement metrics"),
                        " (such as streams, views, likes, and comments).",
                    ],
                    style={"margin": 0, "color": COLORS["muted"], "lineHeight": "1.75", "fontSize": "14px"},
                ),
            ],
        ),

        # ── Dataset ──────────────────────────────────────────────────────────
        _section_title("Dataset"),
        html.P(
            ["The dataset consists of ", html.Strong("26 variables", style={"color": COLORS["text"]}),
             " detailing individual tracks. These can be grouped into three main types of features:"],
            style={"color": COLORS["muted"], "fontSize": "14px", "lineHeight": "1.7", "marginBottom": "14px"},
        ),
        _dataset_badge(
            "Metadata",
            "Track/Artist names, album associations, and release strategies (Album_type like album, single, compilation).",
            _ACCENT,
        ),
        _dataset_badge(
            "Audio Features",
            "11 quantitative metrics mapped by Spotify APIs, including Danceability, Energy, Loudness, Valence (musical positivity), Tempo (BPM), and Duration_ms.",
            _BLUE,
        ),
        _dataset_badge(
            "Engagement Metrics",
            "Cross-platform consumption numbers including Spotify Stream counts alongside YouTube Views, Likes, and Comments.",
            _PURPLE,
        ),

        # ── Analytical Pillars ───────────────────────────────────────────────
        _section_title("Analytical Pillars"),

        # Artist-Level
        _sub_title("Artist-Level Analysis:"),
        _numbered_question(1,
            "Do artists maintain a consistent musical style (Signature Style) across their tracks, "
            "or do they diversify their genres?",
            _ACCENT,
        ),
        _numbered_question(2,
            "How do differences in release strategies (Album_type: album, single, compilation) "
            "affect artist engagement performance?",
            _ACCENT,
        ),
        _numbered_question(3,
            "How do audience engagement metrics (Likes/Views and Comments/Views ratios) on YouTube "
            "vary across artists, and do they positively correlate with Spotify Stream counts?",
            _ACCENT,
        ),
        _numbered_question(4,
            "If we cluster artists based on both musical features and engagement metrics, "
            "what distinct profiles will emerge?",
            _ACCENT,
        ),

        # Song-Level
        _sub_title("Song-Level Analysis:"),
        _numbered_question(1,
            "Does the distribution of audio features (Danceability, Energy, Loudness, etc.) differ "
            "significantly across different release formats (Album_type)?",
            _BLUE,
        ),
        _numbered_question(2,
            "Which audio features (e.g., Tempo, Valence, Loudness) correlate most strongly with "
            "Spotify Streams and YouTube Views?",
            _BLUE,
        ),
        _numbered_question(3,
            "Is there a difference in engagement performance (Views, Likes, Streams) between "
            "short and long tracks?",
            _BLUE,
        ),
        _numbered_question(4,
            "If we use purely technical audio features for clustering, how many \"latent genres\" "
            "will the tracks naturally split into, and how do streams differ across these clusters?",
            _BLUE,
        ),
    ])
