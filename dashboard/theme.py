CARD = {
    "background": "#1e1e2e",
    "borderRadius": "12px",
    "padding": "20px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 16px rgba(0,0,0,0.4)",
}

COLORS = {
    "bg_page": "#12121f",
    "bg_card": "#1e1e2e",
    "bg_subtle": "#2a2a40",
    "accent": "#1db954",
    "text": "#e0e0f0",
    "muted": "#a0a0c0",
}


def dark_layout(title: str = "", height: int = 500) -> dict:
    return {
        "title": {"text": title, "font": {"color": COLORS["text"]}},
        "height": height,
        "paper_bgcolor": COLORS["bg_card"],
        "plot_bgcolor": COLORS["bg_page"],
        "font": {"color": COLORS["text"]},
        "margin": {"t": 50, "l": 40, "r": 20, "b": 40},
        "legend": {"bgcolor": COLORS["bg_card"], "bordercolor": COLORS["bg_subtle"]},
        "coloraxis_colorbar": {"tickfont": {"color": COLORS["text"]}},
    }


def tab_style() -> dict:
    return {
        "backgroundColor": COLORS["bg_card"],
        "color": COLORS["muted"],
        "border": f"1px solid {COLORS['bg_subtle']}",
        "borderRadius": "6px 6px 0 0",
        "padding": "10px 20px",
        "fontWeight": "500",
    }


def tab_selected_style() -> dict:
    return {
        **tab_style(),
        "backgroundColor": COLORS["bg_subtle"],
        "color": COLORS["accent"],
        "borderBottom": f"2px solid {COLORS['accent']}",
    }
