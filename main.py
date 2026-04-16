import os
import datetime
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables (Local) or use Streamlit Secrets (Production)
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID') or st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET') or st.secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI') or st.secrets["SPOTIFY_REDIRECT_URI"]

# Initialize Spotify Client
@st.cache_resource
def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope='user-read-recently-played user-top-read user-read-private user-read-email user-follow-read user-library-read user-read-playback-state user-read-currently-playing'
        )
    )

sp = get_spotify_client()

# UI Configuration
st.set_page_config(page_title="Spotify Analytics", page_icon="🎧", layout='wide')

# --- DATA FETCHING (CACHED FOR PERFORMANCE) ---
@st.cache_data(ttl=3600) # Caches data for 1 hour to reduce API calls
def fetch_top_tracks(time_range='short_term', limit=50):
    tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    if not tracks['items']:
        return pd.DataFrame()
        
    track_ids = [track['id'] for track in tracks['items']]
    audio_features = sp.audio_features(track_ids)
    
    df = pd.DataFrame(audio_features)
    df['track_name'] = [track['name'] for track in tracks['items']]
    df['artist_name'] = [track['artists'][0]['name'] for track in tracks['items']]
    return df[['track_name', 'artist_name', 'danceability', 'energy', 'valence', 'tempo']]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🎧 :green[Dashboard]")
    selected = option_menu(
        "", 
        ["Overview", "Mood Analysis", "Artists", "User"],
        icons=["globe", "activity", "stars", "person"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# --- VIEW: OVERVIEW ---
if selected == "Overview":
    st.title("Market Overview")
    st.markdown("Tracking the corporate performance of leading music streaming infrastructure.")
    
    tickers = {"Spotify": "SPOT", "Apple": "AAPL", "Amazon": "AMZN"}
    selected_tickers = st.multiselect("Select Platforms to Compare", list(tickers.keys()), default=["Spotify"])
    
    if selected_tickers:
        ticker_symbols = [tickers[t] for t in selected_tickers]
        stock_data = yf.download(ticker_symbols, period="1y")['Close']
        
        if len(selected_tickers) == 1:
            stock_data = stock_data.to_frame(name=ticker_symbols[0])
            
        stock_data.reset_index(inplace=True)
        stock_data_melted = stock_data.melt(id_vars='Date', var_name='Stock', value_name='Price')
        
        fig = px.line(
            stock_data_melted, x='Date', y='Price', color='Stock',
            color_discrete_map={'SPOT': '#02ab21', 'AAPL': '#ffffff', 'AMZN': '#146eb4'},
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- VIEW: NEW STATISTICAL ANALYSIS (MOOD QUADRANT) ---
if selected == "Mood Analysis":
    st.title("Behavioral Audio Analysis")
    st.markdown("Mapping your listening habits based on track psychology (Valence vs. Energy).")
    
    time_range = st.radio("Select Time Range", ['short_term', 'medium_term', 'long_term'], horizontal=True, format_func=lambda x: x.replace('_', ' ').title())
    
    df = fetch_top_tracks(time_range=time_range)
    
    if not df.empty:
        fig = px.scatter(
            df, x="valence", y="energy", 
            hover_name="track_name", hover_data=["artist_name"],
            color="danceability", color_continuous_scale=["#121212", "#02ab21"],
            title="Your Audio Mood Quadrant",
            labels={"valence": "Positivity (Valence)", "energy": "Intensity (Energy)"},
            template="plotly_dark"
        )
        
        fig.add_hline(y=0.5, line_dash="dot", line_color="gray")
        fig.add_vline(x=0.5, line_dash="dot", line_color="gray")
        
        fig.add_annotation(x=0.25, y=0.75, text="Angry / Tense", showarrow=False, font=dict(color="white", size=14))
        fig.add_annotation(x=0.75, y=0.75, text="Happy / Energetic", showarrow=False, font=dict(color="#02ab21", size=14))
        fig.add_annotation(x=0.25, y=0.25, text="Sad / Depressing", showarrow=False, font=dict(color="white", size=14))
        fig.add_annotation(x=0.75, y=0.25, text="Chill / Peaceful", showarrow=False, font=dict(color="white", size=14))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Track Data Breakdown")
        st.dataframe(df.style.background_gradient(cmap='Greens', subset=['danceability']), use_container_width=True)
    else:
        st.warning("No track data found for this time range.")

# --- VIEW: ARTISTS (CLEANED UP GRID) ---
if selected == "Artists":
    st.title("Artist Insights")
    followed_artists_response = sp.current_user_followed_artists(limit=8)
    followed_artists = followed_artists_response['artists']['items']
    
    if followed_artists:
        cols = st.columns(4)
        for index, artist in enumerate(followed_artists):
            with cols[index % 4]:
                if artist.get('images'):
                    st.image(artist['images'][0]['url'], use_column_width=True)
                st.markdown(f"**{artist['name']}**")
                st.caption(f"Followers: {artist['followers']['total']:,}")
    else:
        st.info("You don't follow any artists yet.")

# --- VIEW: USER ---
if selected == "User":    
    user_profile = sp.current_user()
    if user_profile:
        col1, col2 = st.columns([1, 2])
        with col1:
            if 'images' in user_profile and user_profile['images']:
                st.image(user_profile['images'][0]['url'], width=200)
            st.subheader(user_profile['display_name'])
            st.caption(f"Followers: {user_profile['followers']['total']}")
            st.markdown(f"**Country:** {user_profile.get('country', 'N/A')}")
            
        with col2:
            current_playback = sp.current_playback()
            if current_playback and current_playback['is_playing']:
                st.success("Currently Listening")
                track = current_playback['item']
                if track and 'album' in track and track['album']['images']:
                    st.image(track['album']['images'][0]['url'], width=100)
                st.markdown(f"### {track['name']}")
                st.markdown(f"**{track['artists'][0]['name']}** — *{track['album']['name']}*")
            else:
                st.info("No active playback detected on your Spotify account right now.")