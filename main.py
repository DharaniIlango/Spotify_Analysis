import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

# --- UI & THEME INITIALIZATION ---
st.set_page_config(page_title="Audio Analytics Deep-Dive", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stProgress > div > div > div > div { background-color: #02ab21; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
    .css-1v0mbdj > img { border-radius: 10px; transition: transform 0.3s ease; }
    .css-1v0mbdj > img:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID') or st.secrets.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET') or st.secrets.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI') or st.secrets.get("SPOTIFY_REDIRECT_URI")

@st.cache_resource
def authenticate_spotify():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope='user-top-read user-read-recently-played user-read-currently-playing'
        )
    )

sp = authenticate_spotify()

# --- DATA PIPELINE ---
@st.cache_data(ttl=3600)
def fetch_analytics_dataset(): 
    # 1. Fetch the first 50 tracks
    tracks_batch_1 = sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
    
    if not tracks_batch_1['items']:
        return pd.DataFrame()
        
    # 2. Fetch the next 50 tracks
    tracks_batch_2 = sp.current_user_top_tracks(limit=50, offset=50, time_range='long_term')
    
    # Combine the two lists to get our 100 tracks for the ML model
    all_tracks = tracks_batch_1['items'] + tracks_batch_2['items']
    
    track_ids = [t['id'] for t in all_tracks]
    
    # 3. Fetch Audio Features in safe batches of 50
    features = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        batch_features = sp.audio_features(batch)
        features.extend([f for f in batch_features if f is not None])
    
    # 4. Merge Data
    df_features = pd.DataFrame(features)
    df_meta = pd.DataFrame([{
        'id': t['id'],
        'name': t['name'],
        'artist': t['artists'][0]['name'],
        'album_cover': t['album']['images'][0]['url'] if t['album']['images'] else None,
        'popularity': t['popularity']
    } for t in all_tracks])
    
    return pd.merge(df_meta, df_features, on='id')

# --- SIDEBAR ROUTING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #02ab21;'>SYNAPSE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>AUDIO INTELLIGENCE</p>", unsafe_allow_html=True)
    st.write("---")
    
    route = option_menu(
        None, ["The Signature", "Psychometrics", "Neural Clustering", "Visual Vault"],
        icons=["radar", "activity", "cpu", "grid"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#02ab21", "font-weight": "300"},
        }
    )

df = fetch_analytics_dataset(limit=100)

if df.empty:
    st.warning("Insufficient data to build analytical models. Keep listening to music!")
    st.stop()

# --- VIEW 1: THE SIGNATURE ---
if route == "The Signature":
    st.markdown("### Your Sonic Identity")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        categories = ['acousticness', 'danceability', 'energy', 'liveness', 'valence']
        avg_features = df[categories].mean().tolist()
        avg_features += [avg_features[0]]
        categories += [categories[0]]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=avg_features, theta=[c.capitalize() for c in categories],
            fill='toself', fillcolor='rgba(2, 171, 33, 0.4)', line=dict(color='#02ab21', width=2),
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor="#333333"),
                angularaxis=dict(gridcolor="#333333", tickfont=dict(color="white", size=14)),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)", height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("#### System Overview")
        st.metric(label="Total Tracks Analyzed", value=len(df))
        st.metric(label="Average BPM (Tempo)", value=f"{df['tempo'].mean():.0f}")
        
        current = sp.current_user_playing_track()
        if current and current['is_playing']:
            st.write("---")
            st.markdown("🟢 **Active Stream Detected**")
            st.caption(f"{current['item']['name']} - {current['item']['artists'][0]['name']}")

# --- VIEW 2: PSYCHOMETRICS ---
elif route == "Psychometrics":
    st.markdown("### Behavioral Heatmaps")
    fig_heat = px.density_heatmap(
        df, x="tempo", y="energy", nbinsx=15, nbinsy=15,
        color_continuous_scale=["#0E1117", "#054211", "#02ab21", "#42ff65"],
        labels={"tempo": "Beats Per Minute", "energy": "Acoustic Energy"}
    )
    fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig_heat, use_container_width=True)

# --- VIEW 3: NEURAL CLUSTERING (MACHINE LEARNING) ---
elif route == "Neural Clustering":
    st.markdown("### Unsupervised Vibe Clustering")
    st.markdown("Using K-Means to autonomously group your music based on audio geometry, overriding standard genres.")
    
    # 1. Prepare and Scale the Data
    ml_features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
    X = df[ml_features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Apply K-Means Algorithm
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    df['Cluster_Name'] = df['Cluster'].apply(lambda x: f"Vibe Cluster {x+1}")
    
    # 3. 3D Plotly Visualization
    fig_cluster = px.scatter_3d(
        df, x='valence', y='energy', z='danceability',
        color='Cluster_Name', hover_name='name', hover_data=['artist'],
        color_discrete_sequence=["#02ab21", "#ffffff", "#555555", "#888888"],
        title="3D Sonic Landscape"
    )
    fig_cluster.update_layout(
        scene=dict(
            xaxis_title='Positivity (Valence)', yaxis_title='Intensity (Energy)', zaxis_title='Groove',
            xaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
            yaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
            zaxis=dict(backgroundcolor="#0E1117", gridcolor="#333", showbackground=True),
        ),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), height=600,
        legend=dict(title="")
    )
    st.plotly_chart(fig_cluster, use_container_width=True)
    
    # 4. Display the AI Groupings
    st.markdown("### The AI's Groupings")
    tabs = st.tabs([f"Cluster {i+1}" for i in range(num_clusters)])
    
    for i, tab in enumerate(tabs):
        with tab:
            cluster_df = df[df['Cluster'] == i][['name', 'artist', 'tempo', 'popularity']]
            st.dataframe(cluster_df.reset_index(drop=True), use_container_width=True)

# --- VIEW 4: VISUAL VAULT ---
elif route == "Visual Vault":
    st.markdown("### The Visual Vault")
    st.write("---")
    
    num_cols = 4
    cols = st.columns(num_cols)
    
    for i, row in df.iterrows():
        if row['album_cover']:
            with cols[i % num_cols]:
                st.image(row['album_cover'], use_column_width=True)
                st.markdown(f"<p style='font-size: 0.85em; text-align: center; margin-top: -10px;'><b>{row['name']}</b><br><span style='color: gray;'>{row['artist']}</span></p>", unsafe_allow_html=True)
                st.write("")