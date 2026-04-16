import os
import spotipy  # Fix: Import as a standard module to avoid variable name conflict
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

# --- 1. UI CONFIGURATION (MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="Synapse Audio Intelligence", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

# --- 2. THEME & STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stProgress > div > div > div > div { background-color: #02ab21; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
    .css-1v0mbdj > img { border-radius: 10px; transition: transform 0.3s ease; }
    .css-1v0mbdj > img:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- 3. AUTHENTICATION & CLIENT INITIALIZATION ---
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID') or st.secrets.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET') or st.secrets.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI') or st.secrets.get("SPOTIFY_REDIRECT_URI")

@st.cache_resource
def authenticate_spotify():
    """Initializes and returns the authenticated Spotify client."""
    all_scopes = (
        'user-read-private user-read-email user-library-read '
        'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public '
        'user-top-read user-read-recently-played user-read-playback-position '
        'user-read-playback-state user-modify-playback-state user-read-currently-playing '
        'user-follow-read'
    )
    
    # Return an instance of the Spotify client
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=all_scopes
        )
    )

# Initialize the client globally as 'spotify_client' to avoid confusion
spotify_client = authenticate_spotify()

# --- 4. DATA PIPELINE (UPGRADED FOR AUDIOPHILE PLAYLISTS) ---
@st.cache_data(ttl=3600)
def get_user_playlists():
    """Fetches the user's playlists for the sidebar dropdown."""
    # Use the initialized client instance
    playlists_data = spotify_client.current_user_playlists(limit=50)
    return {p['name']: p['id'] for p in playlists_data.get('items', []) if p is not None}

@st.cache_data(ttl=3600)
def fetch_analytics_dataset(source_id="top_tracks"): 
    """Extracts metadata from Top Tracks or a specific Playlist ID."""
    all_tracks = []
    
    if source_id == "top_tracks":
        # Fetches user's long-term top tracks in two batches
        t1 = spotify_client.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
        t2 = spotify_client.current_user_top_tracks(limit=50, offset=50, time_range='long_term')
        all_tracks = t1.get('items', []) + t2.get('items', [])
    else:
        # Audiophile Logic: Infinite loop to extract 200+ song playlists
        offset = 0
        while True:
            results = spotify_client.playlist_items(source_id, limit=100, offset=offset)
            items = results.get('items', [])
            if not items:
                break
            
            valid_tracks = [item['track'] for item in items if item and item.get('track')]
            all_tracks.extend(valid_tracks)
            
            if len(items) < 100:
                break
            offset += 100
            
    # Extract metadata safely (Pivoted to metadata to avoid deprecated audio_features endpoint)
    data = []
    for t in all_tracks:
        if not t: 
            continue
            
        album = t.get('album', {})
        release_date = album.get('release_date', '')
        release_year = int(release_date.split('-')[0]) if release_date else 2000
        
        images = album.get('images', [])
        album_cover = images[0]['url'] if images else None
        
        artists = t.get('artists', [])
        artist_name = artists[0]['name'] if artists else "Unknown Artist"
        
        data.append({
            'id': t.get('id', 'local_or_unknown'),
            'name': t.get('name', 'Unknown Track'),
            'artist': artist_name,
            'album_cover': album_cover,
            'popularity': t.get('popularity', 0),
            'duration_m': t.get('duration_ms', 0) / 60000,
            'explicit': 1 if t.get('explicit') else 0,
            'release_year': release_year
        })
        
    return pd.DataFrame(data)

# --- 5. SIDEBAR NAVIGATION & ROUTING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #02ab21;'>SYNAPSE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>AUDIO INTELLIGENCE</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🎛️ Data Source")
    
    # Dropdown for playlist selection
    user_playlists = get_user_playlists()
    source_options = {"🏆 My All-Time Top Tracks": "top_tracks"}
    source_options.update(user_playlists)
    
    selected_source_name = st.selectbox("Select Target:", list(source_options.keys()))
    selected_source_id = source_options[selected_source_name]
    
    st.write("---")
    
    route = option_menu(
        None, ["The Profile", "Temporal Dynamics", "Neural Clustering", "Visual Vault"],
        icons=["person-lines-fill", "clock-history", "cpu", "grid"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#02ab21", "font-weight": "300"},
        }
    )

# Load the dataset based on selection
df = fetch_analytics_dataset(source_id=selected_source_id)

if df.empty:
    st.warning("No track data found in this source. Keep listening to music!")
    st.stop()

# --- 6. MAIN DASHBOARD VIEWS ---

# VIEW 1: THE PROFILE
if route == "The Profile":
    st.markdown("### Your Sonic Identity")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Avg Popularity", value=f"{df['popularity'].mean():.1f}/100")
    with col2:
        st.metric(label="Avg Release Era", value=f"{int(df['release_year'].mean())}")
    with col3:
        st.metric(label="Avg Duration", value=f"{df['duration_m'].mean():.2f} min")
        
    st.write("---")
    st.markdown("#### Top Artists by Track Count")
    artist_counts = df['artist'].value_counts().head(10).reset_index()
    artist_counts.columns = ['Artist', 'Track Count']
    fig_bar = px.bar(
        artist_counts, x='Track Count', y='Artist', orientation='h',
        color='Track Count', color_continuous_scale=["#0E1117", "#02ab21"],
        template="plotly_dark"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

# VIEW 2: TEMPORAL DYNAMICS
elif route == "Temporal Dynamics":
    st.markdown("### Nostalgia vs. Mainstream")
    fig_scatter = px.scatter(
        df, x="release_year", y="popularity", 
        size="duration_m", color="explicit",
        hover_name="name", hover_data=["artist"],
        color_continuous_scale=["#02ab21", "#ff4b4b"],
        labels={"release_year": "Release Year", "popularity": "Fame Index (Popularity)"},
        template="plotly_dark"
    )
    fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

# VIEW 3: NEURAL CLUSTERING (MACHINE LEARNING)
elif route == "Neural Clustering":
    st.markdown("### Unsupervised Metadata Clustering")
    
    # Scaling and Clustering
    ml_features = ['popularity', 'duration_m', 'release_year']
    X_scaled = StandardScaler().fit_transform(df[ml_features])
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    df['Cluster_Name'] = df['Cluster'].apply(lambda x: f"Cluster {x+1}")
    
    fig_cluster = px.scatter_3d(
        df, x='release_year', y='popularity', z='duration_m',
        color='Cluster_Name', hover_name='name', hover_data=['artist'],
        color_discrete_sequence=["#02ab21", "#ffffff", "#555555", "#888888"]
    )
    fig_cluster.update_layout(
        scene=dict(
            xaxis_title='Era (Year)', yaxis_title='Fame (Popularity)', zaxis_title='Length (Mins)',
            xaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
            yaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
            zaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
        ),
        paper_bgcolor="rgba(0,0,0,0)", height=700
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

# VIEW 4: VISUAL VAULT
elif route == "Visual Vault":
    st.markdown("### The Visual Vault")
    num_cols = 4
    cols = st.columns(num_cols)
    for i, row in df.iterrows():
        if row['album_cover']:
            with cols[i % num_cols]:
                st.image(row['album_cover'], use_column_width=True)
                st.markdown(f"<p style='font-size: 0.85em; text-align: center;'><b>{row['name']}</b><br>{row['artist']}</p>", unsafe_allow_html=True)