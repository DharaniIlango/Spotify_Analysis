import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import plotly.express as px

CLIENT_ID = '5d865840417549cc8b9a00ebd3694805'
CLIENT_SECRET = '7f83017d8f0b43a89dfa7732ad6ca195'
REDIRECT_URI = "http://localhost:5000"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-read-recently-played user-top-read'
    )
)

st.set_page_config(page_title="Spotify Song Analytics", page_icon=":musical_note:")
st.title("Analysis of Your TOP Tracks")
st.write("Diving into the Exploration of your Top Tracks")

# Function to get top genres
def get_genres(sp, track_ids):
    genres = []
    for track_id in track_ids:
        track = sp.track(track_id)
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        genres.extend(artist['genres'])
    return genres

# Function to visualize genres 
def visualize_genres(genres):
    # Count the occurrences of each genre
    genre_counts = pd.Series(genres).value_counts().head(10)
    df = pd.DataFrame({
        'Genre': genre_counts.index,
        'Count': genre_counts.values
    })
    fig = px.pie(df, values='Count', names='Genre', title="Top Genres")
    st.plotly_chart(fig, use_container_width=True)


# Function to get top artists
def get_top_artists(sp, time_range):
    results = sp.current_user_top_artists(time_range=time_range, limit=20)
    return results['items']

def visualize_top_artists(artists):
    # Extract artist names and follower counts
    artist_names = [artist['name'] for artist in artists]
    followers = [artist['followers']['total'] for artist in artists]
    # Create a DataFrame for visualization
    df = pd.DataFrame({
        'Artist': artist_names,
        'Followers': followers
    })
    # Create a pie chart using Plotly
    fig = px.pie(df, values='Followers', names='Artist', title="Top Artists by Follower Count")
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Main Streamlit app
def main():
    st.subheader("Your Listening Findings")

    # Fetch user profile
    user = sp.current_user()
    st.sidebar.subheader("User Profile")
    st.sidebar.write(f"Name: {user['display_name']}")

    # Fetch listening history
    history = sp.current_user_recently_played(limit=50)

    # Preprocess data
    track_ids = [item['track']['id'] for item in history['items']]
    
    st.header("Genres")
    genres = get_genres(sp, track_ids)
    visualize_genres(genres)
    
    st.header("Artists")
    artists = get_top_artists(sp, time_range="long_term")
    visualize_top_artists(artists)

#Short_Term_Analytics
top_tracks_short_term = sp.current_user_top_tracks(limit=20, time_range='short_term')
track_ids_short_term = [track['id'] for track in top_tracks_short_term['items']]
audio_features_short_term = sp.audio_features(track_ids_short_term)

df_short = pd.DataFrame(audio_features_short_term)
df_short['track_name'] = [track['name'] for track in top_tracks_short_term['items']]
df_short = df_short[['track_name', 'danceability', 'energy', 'valence']]
df_short.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Short Term')
st.bar_chart(df_short, height=650)

#Medium_Term_Analytics
top_tracks_medium_term = sp.current_user_top_tracks(limit=20, time_range='medium_term')
track_ids_medium_term = [track['id'] for track in top_tracks_medium_term['items']]
audio_features_medium_term = sp.audio_features(track_ids_medium_term)

df_medium = pd.DataFrame(audio_features_medium_term)
df_medium['track_name'] = [track['name'] for track in top_tracks_medium_term['items']]
df_medium = df_medium[['track_name', 'danceability', 'energy', 'valence']]
df_medium.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Medium Term')
st.bar_chart(df_medium, height=650)

#Long_Term_Analysis
top_tracks_long_term = sp.current_user_top_tracks(limit=25, time_range='long_term')
track_ids_long_term = [track['id'] for track in top_tracks_long_term['items']]
audio_features_long_term = sp.audio_features(track_ids_long_term)

df_long = pd.DataFrame(audio_features_long_term)
df_long['track_name'] = [track['name'] for track in top_tracks_long_term['items']]
df_long = df_long[['track_name', 'danceability', 'energy', 'valence']]
df_long.set_index('track_name', inplace=True)

st.subheader('Audio Features of Top Tracks in Long Term')
st.bar_chart(df_long, height=650)


if __name__ == "__main__":
    main()