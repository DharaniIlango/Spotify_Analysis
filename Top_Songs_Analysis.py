import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5000"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )
)

st.set_page_config(page_title="Spotify Song Analytics", page_icon=":musical_note:")
st.title("Analysis of Your TOP Tracks")
st.write("Diving into the Exploration of your Top Tracks")

#Short_Term_Analytics
top_tracks_short_term = sp.current_user_top_tracks(limit=10, time_range='short_term')
track_ids_short_term = [track['id'] for track in top_tracks_short_term['items']]
audio_features_short_term = sp.audio_features(track_ids_short_term)

df_short = pd.DataFrame(audio_features_short_term)
df_short['track_name'] = [track['name'] for track in top_tracks_short_term['items']]
df_short = df_short[['track_name', 'danceability', 'energy', 'valence']]
df_short.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Short Term')
st.bar_chart(df_short, height=700)

#Medium_Term_Analytics
top_tracks_medium_term = sp.current_user_top_tracks(limit=20, time_range='medium_term')
track_ids_medium_term = [track['id'] for track in top_tracks_medium_term['items']]
audio_features_medium_term = sp.audio_features(track_ids_medium_term)

df_medium = pd.DataFrame(audio_features_medium_term)
df_medium['track_name'] = [track['name'] for track in top_tracks_medium_term['items']]
df_medium = df_medium[['track_name', 'danceability', 'energy', 'valence']]
df_medium.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Medium Term')
st.bar_chart(df_medium, height=700)

#Long_Term_Analysis
top_tracks_long_term = sp.current_user_top_tracks(limit=25, time_range='long_term')
track_ids_long_term = [track['id'] for track in top_tracks_long_term['items']]
audio_features_long_term = sp.audio_features(track_ids_long_term)

df_long = pd.DataFrame(audio_features_long_term)
df_long['track_name'] = [track['name'] for track in top_tracks_long_term['items']]
df_long = df_long[['track_name', 'danceability', 'energy', 'valence']]
df_long.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Long Term')
st.bar_chart(df_long, height=700)