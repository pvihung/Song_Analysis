"""
Data Observation tab — raw data snapshot, shape, dtypes, null counts,
descriptive statistics, and a paginated interactive table.
"""

import pandas as pd
from dash import dash_table, dcc, html

from dashboard.data import AUDIO_FEATURES, ENGAGEMENT
from dashboard.theme import CARD, COLORS, dark_layout


def _info_card(label: str, value: str) -> html.Div:
    return html.Div(
        style={
            **CARD,
            "textAlign": "center",
            "padding": "16px",
            "marginBottom": 0,
        },
        children=[
            html.P(
                label,
                style={
                    "margin": 0,
                    "fontSize": "11px",
                    "textTransform": "uppercase",
                    "letterSpacing": "1px",
                    "opacity": 0.6,
                },
            ),
            html.H3(value, style={"margin": "6px 0 0", "color": COLORS["accent"]}),
        ],
    )


def _table(data: pd.DataFrame, table_id: str, page_size: int = 12) -> dash_table.DataTable:
    return dash_table.DataTable(
        id=table_id,
        data=data.to_dict("records"),
        columns=[{"name": c, "id": c} for c in data.columns],
        page_size=page_size,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "backgroundColor": COLORS["bg_page"],
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['bg_subtle']}",
            "fontSize": "12px",
            "padding": "6px 10px",
        },
        style_header={
            "backgroundColor": COLORS["bg_subtle"],
            "fontWeight": "bold",
            "color": COLORS["accent"],
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": COLORS["bg_card"]}
        ],
    )


def layout(df: pd.DataFrame) -> html.Div:
    # ── Null summary ─────────────────────────────────────────────────────────
    null_df = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str).values,
        "Non-Null": df.notna().sum().values,
        "Null Count": df.isna().sum().values,
        "Null %": (df.isna().mean() * 100).round(2).values,
    })

    # ── Descriptive stats ────────────────────────────────────────────────────
    stats_df = (
        df[AUDIO_FEATURES + ENGAGEMENT]
        .describe()
        .round(3)
        .reset_index()
        .rename(columns={"index": "stat"})
    )

    return html.Div([
        # KPI row
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "16px",
                "marginBottom": "20px",
            },
            children=[
                _info_card("Total Rows", f"{len(df):,}"),
                _info_card("Total Columns", str(df.shape[1])),
                _info_card("Artists", f"{df['Artist'].nunique():,}"),
                _info_card("Unique Tracks", f"{df['Track'].nunique():,}"),
            ],
        ),

        # Column info / null table
        html.Div(style=CARD, children=[
            html.H4("Column Overview — Null Report", style={"marginTop": 0, "color": COLORS["text"]}),
            _table(null_df, "null-table", page_size=15),
        ]),

        # Descriptive statistics
        html.Div(style=CARD, children=[
            html.H4("Descriptive Statistics — Audio Features & Engagement", style={"marginTop": 0, "color": COLORS["text"]}),
            _table(stats_df, "stats-table", page_size=10),
        ]),

        # Raw data sample
        html.Div(style=CARD, children=[
            html.H4("Raw Data Sample (first 500 rows)", style={"marginTop": 0, "color": COLORS["text"]}),
            _table(df.head(500).round(4).reset_index(drop=True), "raw-table", page_size=12),
        ]),
    ])
