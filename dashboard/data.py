import pandas as pd
import numpy as np

AUDIO_FEATURES = [
    "Danceability", "Energy", "Loudness", "Speechiness",
    "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo",
]
ENGAGEMENT = ["Stream", "Views", "Likes", "Comments"]
CATEGORICAL = ["Album_type", "Key"]
ALBUM_COLORS = {"album": "#636EFA", "single": "#EF553B", "compilation": "#00CC96"}

DROP_COLS = ["Url_spotify", "Uri", "Url_youtube", "Description", "Title", "Channel"]


def load_data(path: str = "sample_data/Spotify_Youtube.csv") -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = df[df["Licensed"] == True].copy()

    for col in AUDIO_FEATURES + ENGAGEMENT:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in CATEGORICAL:
        df[col] = df[col].astype("category")

    df = df.drop_duplicates(subset=AUDIO_FEATURES, keep="first")
    df = df.dropna(subset=AUDIO_FEATURES)
    df = df.reset_index(drop=True)

    for col in ENGAGEMENT:
        df[f"log_{col}"] = np.log1p(df[col])

    df["Engagement_rate"] = df["Likes"] / df["Views"].replace(0, np.nan)

    return df


def artist_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Artist", observed=True)
        .agg(
            Track_count=("Track", "count"),
            Total_Streams=("Stream", "sum"),
            Total_Views=("Views", "sum"),
            Avg_Streams=("Stream", "mean"),
            Avg_Views=("Views", "mean"),
        )
        .reset_index()
        .sort_values("Total_Streams", ascending=False)
    )
