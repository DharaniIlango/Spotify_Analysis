import datetime
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import altair as alt
import pandas as pd
import plotly.express as px

CLIENT_ID = '5d865840417549cc8b9a00ebd3694805'
CLIENT_SECRET = '7f83017d8f0b43a89dfa7732ad6ca195'
REDIRECT_URI = "https://spotify-profile-analysis.netlify.app/callback"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-read-recently-played user-top-read user-read-private user-read-email user-follow-read user-library-read user-read-playback-state user-read-currently-playing'
    )
)

st.set_page_config(
    page_title="Spotify Song Analytics", 
    page_icon=":musical_keyboard:", 
    layout='wide',
    initial_sidebar_state = "expanded"
    )

st.markdown("# 🎧 :green[Spotify] : Music For Everyone")

with st.sidebar:
    selected = option_menu("Spotify Dashboard", ["Overview", "Top Songs", "Artists", "Genres", "User"],
                           icons=["globe-central-south-asia","music-note-list","stars","signpost-split-fill","person-circle"],
                           menu_icon="spotify",
                           default_index=0,
                           styles={
                                "container": {"padding": "2","background-color":'black'},
                                "icon": {"color": "white", "font-size": "20px"}, 
                                "nav-link": {"color":"white","font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#1DD2"},
                                "nav-link-selected": {"background-color": "#02ab21"},}
                           )
    
#Menu 1 - Spotify Overview
if selected == "Overview":
    st.markdown("### Explore insights into your Spotify usage and preferences.")
    col1, _, col2 = st.columns([3, 0.5, 3])
    with col1:
        st.header("About")
        text = """
            <div style="text-align: justify; font-size: 20px;">
            Launched in 2008, Spotify is a leading music streaming platform that offers a vast library of songs, podcasts, playlists, and more. Users can discover new music, create playlists, and enjoy personalized recommendations. Spotify connects artists and listeners, providing a platform for music discovery and enjoyment.
            </div>
            """
        st.markdown(text, unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        url = "https://open.spotify.com/"
        if st.button("Get Your App Now"):
            webbrowser.open_new_tab(url)
    with col2:
        st.header("Stock Value")
        ticker_symbol = "SPOT"
        ticker_data = yf.Ticker(ticker_symbol)
        ticker_df = ticker_data.history(period='1y', interval='1h')
        chart = alt.Chart(ticker_df.reset_index()).mark_line(color='#02ab21').encode(
                        x='Datetime:T',
                        y='Close:Q'
                    ).properties(
                        width=800,
                        height=400
                    )
        st.altair_chart(chart, use_container_width=True)
        
    column1, _, column2 = st.columns([3, 0.1, 3])
    with column1:
        st.header("Goals")
        text = """
            <div style="text-align: justify; font-size: 20px;">
                <ul>
                    <li> Enhancing user <span style="color: #02ab21">Engagement</span> </li>
                    <li> Curating high-quality <span style="color: #02ab21">Content</span> </li>
                    <li> Improving <span style="color: #02ab21">Accessibility</span> and <span style="color: #02ab21">Personalization</span> </li>
                    <li> Innovating in <span style="color: #02ab21">Music Discovery</span> </li>
                </ul>
            </div>
            """
        st.markdown(text, unsafe_allow_html=True)
    with column2:
        st.write("")
        st.write("")
        st.image("./Assets/Spotify_Full_Logo_RGB_Green.png")
            
    switch_stock_comparision = st.toggle("View Stock Comparisons")
    if switch_stock_comparision:
        # Fetch stock data
        def fetch_stock_data(tickers, period="1y"):
            stock_data = {}
            for ticker in tickers:
                stock_data[ticker] = yf.Ticker(ticker).history(period=period)['Close']
            return pd.DataFrame(stock_data)

        # Plot stock data
        def plot_stock_data(stock_data):
            stock_data.reset_index(inplace=True)
            stock_data = stock_data.melt(id_vars='Date', var_name='Stock', value_name='Price')
            fig = px.line(stock_data, x='Date', y='Price', color='Stock', title='Stock Price Comparison',
                        color_discrete_map={'SPOT': '#02ab21', 'AAPL': '#b166cc', 'AMZN': '#146eb4'})
            st.plotly_chart(fig)
            
        st.header("Comparative Stock Line Graph of Music Platforms")
        tickers = {
                "Spotify": "SPOT",
                "Apple": "AAPL",
                "Amazon": "AMZN",
            }
        selected_tickers = st.multiselect("Select Music Platforms to Compare", list(tickers.keys()), default=list(tickers.keys()))
            
        if selected_tickers:
            ticker_symbols = [tickers[ticker] for ticker in selected_tickers]
            period = st.selectbox("Select Time Period", ["1y", "6mo", "3mo", "1mo"], index=0)
                
            stock_data = fetch_stock_data(ticker_symbols, period)
            st.subheader(f"Stock Price Comparison for the Last {period}")
            plot_stock_data(stock_data)
    

#Menu 2 - Top Songs Section
if selected == "Top Songs":
    top_song_choice = st.multiselect(
        "Choose the Range for Analysis",
        ["Short Term", "Medium Term", "Long Term"],
        ["Short Term"],
    )
    def top_song_short_term():
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
        
    def top_song_medium_term():
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

    def top_song_long_term():
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

    for choice in top_song_choice:
        if choice=="Short Term":
            top_song_short_term()
        if choice=="Medium Term":
            top_song_medium_term()
        if choice=="Long Term":
            top_song_long_term()
    
#Menu 3 - Artists Section
if selected == "Artists":
    # Main application
    st.title("Artist Analysis on Spotify")

    # Display user's followed artists in a grid layout with charts
    st.header("Followed Artists")
    # Function to fetch followed artists
    def fetch_followed_artists():
        followed_artists = sp.current_user_followed_artists(limit=20)['artists']['items']
        return followed_artists

    # Function to fetch recently played artists
    def fetch_recently_played_artists():
        recently_played_tracks = sp.current_user_recently_played(limit=20)['items']
        recently_played_artists = []
        for item in recently_played_tracks:
            artist = item['track']['artists'][0]  # Assuming only one artist per track for simplicity
            if artist not in recently_played_artists:
                recently_played_artists.append(artist)
        return recently_played_artists

    # Function to fetch top tracks of an artist
    def fetch_top_tracks(artist_id):
        top_tracks = sp.artist_top_tracks(artist_id)['tracks']
        return top_tracks

    followed_artists = fetch_followed_artists()

    if followed_artists:
        for artist in followed_artists:
            st.subheader(artist['name'])
            if artist.get('images'):  # Check if 'images' key exists
                st.image(artist['images'][0]['url'], caption=artist['name'], width=200)
            
            # Fetch and display top tracks of the artist
            top_tracks = fetch_top_tracks(artist['id'])
            if top_tracks:
                st.subheader(f"Top Tracks of {artist['name']}")
                for track in top_tracks:
                    st.write(f"- {track['name']} ({track['album']['name']})")
            
            st.write("---")  # Separator between artists

    else:
        st.write("No followed artists found.")

    # Display user's recently played artists in a grid layout with charts
    st.header("Recently Played Artists")

    recently_played_artists = fetch_recently_played_artists()

    if recently_played_artists:
        for artist in recently_played_artists:
            st.subheader(artist['name'])
            if artist.get('images'):  # Check if 'images' key exists
                st.image(artist['images'][0]['url'], caption=artist['name'], width=200)
            
            # Fetch and display top tracks of the artist
            top_tracks = fetch_top_tracks(artist['id'])
            if top_tracks:
                st.subheader(f"Top Tracks of {artist['name']}")
                for track in top_tracks:
                    st.write(f"- {track['name']} ({track['album']['name']})")
            
            st.write("---")  # Separator between artists

    else:
        st.write("No recently played artists found.")

#Menu 4 - Genres Section
if selected == "Genres":
    # Function to fetch user's top tracks
    def fetch_top_tracks(limit=10):
        top_tracks = sp.current_user_top_tracks(limit=limit, time_range='medium_term')
        return top_tracks['items']

    # Function to fetch user's top artists
    def fetch_top_artists(limit=10):
        top_artists = sp.current_user_top_artists(limit=limit, time_range='medium_term')
        return top_artists['items']

    # Function to fetch user's recently played tracks
    def fetch_recently_played(limit=10):
        recent_tracks = sp.current_user_recently_played(limit=limit)
        return recent_tracks['items']

    # Function to fetch user's top genres
    def fetch_top_genres(limit=5):
        top_artists = fetch_top_artists(limit)
        genres = []
        for artist in top_artists:
            for genre in artist['genres']:
                genres.append(genre)
        genre_counts = pd.Series(genres).value_counts().head(limit)
        return genre_counts

    # Streamlit UI
    st.title("Spotify User Listening Analysis")

    # Fetch user's top tracks, artists, and recently played tracks
    top_tracks = fetch_top_tracks()
    top_artists = fetch_top_artists()
    recent_tracks = fetch_recently_played()

    # Display user's top genres using a pie chart
    top_genres = fetch_top_genres()
    if not top_genres.empty:
        st.header("Top Genres")
        fig_genres = px.pie(values=top_genres.values, names=top_genres.index, title='Top Genres',
                        color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_genres)

    # Display user's top tracks
    if top_tracks:
        st.header("Top Tracks")
        track_names = [track['name'] for track in top_tracks]
        track_popularities = [track['popularity'] for track in top_tracks]
        df_tracks = pd.DataFrame({'Track Name': track_names, 'Popularity': track_popularities})
        st.write(df_tracks)

        # Plot top tracks with custom color
        fig_tracks = px.bar(df_tracks, x='Track Name', y='Popularity', title='Top Tracks',
                            color_discrete_sequence=['#1DB954'])  # Set the color to Spotify green
        st.plotly_chart(fig_tracks)


    # Display user's top artists
    if top_artists:
        st.header("Top Artists")
        artist_names = [artist['name'] for artist in top_artists]
        artist_followers = [artist['followers']['total'] for artist in top_artists]
        df_artists = pd.DataFrame({'Artist Name': artist_names, 'Followers': artist_followers})
        st.write(df_artists)

        # Plot top artists
        fig_artists = px.bar(df_artists, x='Artist Name', y='Followers', title='Top Artists',
                            color_discrete_sequence=['#1DB954'])
        st.plotly_chart(fig_artists)

    # Display user's recently played tracks
    if recent_tracks:
        st.header("Recently Played Tracks")
        recent_track_names = [track['track']['name'] for track in recent_tracks]
        recent_artists = [", ".join([artist['name'] for artist in track['track']['artists']]) for track in recent_tracks]
        df_recent_tracks = pd.DataFrame({'Track Name': recent_track_names, 'Artists': recent_artists})
        st.write(df_recent_tracks)

        # Plot recently played tracks
        fig_recent_tracks = px.bar(df_recent_tracks, x='Track Name', y='Artists', title='Recently Played Tracks', 
                                labels={'Track Name': 'Track Name', 'Artists': 'Artists'},
                                color_discrete_sequence=['#1DB954'])
        st.plotly_chart(fig_recent_tracks)    

#Menu 5 - User Section
if selected == "User":    
    user_profile = sp.current_user()
    playlists = sp.current_user_playlists()
    recently_played = sp.current_user_recently_played(limit=50)
    playing_track = sp.current_user_playing_track()

    if user_profile:
        st.markdown(f"### {user_profile['display_name']}'s Profile")
        st.markdown("---")
        col1, col2= st.columns(2)
        with col1:
            st.markdown("## User Bio")
            # Display profile picture if available
            if 'images' in user_profile and len(user_profile['images']) > 0:
                st.image(user_profile['images'][0]['url'], caption='Profile Picture', width=150)

            # Display profile details
            st.markdown(f"**Email:** {user_profile['email']}")
            st.markdown(f"**Followers:** {user_profile['followers']['total']}")
            st.markdown(f"**Country:** {user_profile['country']}")
            st.markdown(f"**Spotify Profile:** [Link]({user_profile['external_urls']['spotify']})")
            st.markdown(f"**Number of Playlists:** {playlists['total']}")
            total_listening_time = 0
            for item in recently_played['items']:
                track = item['track']
                # Calculate total listening time
                total_listening_time += track['duration_ms'] / 1000  # convert milliseconds to seconds

                # Convert total listening time to hours, minutes, and seconds
            total_listening_time_str = str(datetime.timedelta(seconds=int(total_listening_time)))
            st.markdown(f"**Total Listening Time (Last 24 hours):** {total_listening_time_str}")
            
        with col2:
            # Display currently playing track
            current_playback = sp.current_playback()
            if current_playback and current_playback['is_playing']:
                track = current_playback['item']
                st.markdown("## Currently Playing")
                st.image(track['album']['images'][0]['url'], width=150)
                st.markdown(f"**Track:** {track['name']}")
                st.markdown(f"**Artist:** {', '.join([artist['name'] for artist in track['artists']])}")
                st.markdown(f"**Album:** {track['album']['name']}")
            else:
                st.markdown("No track is currently playing.")
                
        with col2:
            # Display recently played track
            if recently_played and recently_played['items']:
                track = recently_played['items'][0]['track']
                st.markdown("## Recently Played")
                st.image(track['album']['images'][0]['url'], width=150)
                st.markdown(f"**Track:** {track['name']}")
                st.markdown(f"**Artist:** {', '.join([artist['name'] for artist in track['artists']])}")
                st.markdown(f"**Album:** {track['album']['name']}")
            else:
                st.markdown("No recently played tracks found.")
    else:
        st.write("Unable to retrieve user profile.")
