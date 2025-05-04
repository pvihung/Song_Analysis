# Music_Analysis
***Group Members***: Hung Pham, Linh Pham, Arthur Roth

***Course***:  CS133  

---
## Overview:
This project explores the relationship between audio features of songs and their streaming performance on Spotify and YouTube. By combining Exploratory Data Analysis (EDA), clustering, and regression modeling, we aim to understand what makes a song popular and build a basic song recommender system to help users discover similar tracks based on their preferences.

---
## Project Objectives
### 1.  EDA:      
- What are the top 10 songs on Spotify and YouTube? 
- Do high-tempo songs garner more streams?
- Do songs with longer or shorter titles have more streams on average?
- Which traits make a loud song (danceability, energy, tempo, etc.) widely streamed vs a quiet song?
- Which combinations of valence and tempo create the most streamed songs? Are songs with high valence and low tempo most popular, or is it another combination, like low valence and high tempo?

  
### 2. Machine Learning Model: 
We will work on:
- Extracting and visualize which audio traits (e.g., loudness, valence, acousticness) matter most in determining popularity. This supports strategic decisions in song production or recommendation by finding other songs in the same cluster with high cosine similarity.
- Creating a ***song recommender*** using **K-Means Clustering** model. It will be able to suggest some song recommendation for user based on the song they like.

---
## Data Description:
This dataset of songs of various artist in the world and for each song is present:
- Characteristic of a song, such as Danceability, Energy, Loudness, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, Tempo,...
- Several statistics of the music version on spotify, including the number of streams, number of views of the official music video of the song on youtube.

**Source**: https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube/data

--- 
## Installation & Setup
To run this project:
1. Clone the repository or download the notebook.
2. Install required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn xgboost

