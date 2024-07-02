# Spotify Top Songs Analysis

## Project Description
The Spotify Analysis Dashboard is a robust application built using Python and Streamlit, designed to provide users with detailed insights into their Spotify usage and music preferences. Leveraging Spotify's API and a range of powerful data visualization libraries, this dashboard offers a comprehensive view of your top songs, artists, genres, and more.

## Key Features

- **Top Song Analysis:** Explore your favorite tracks categorized into short-term, medium-term, and long-term periods. Each track's audio features such as danceability, energy, and valence are analyzed and visualized using interactive bar charts.
- **Market Comparison:** Gain insights into Spotify's stock performance over time, compared with other major music platforms. This feature uses Yahoo Finance data and presents the data with interactive line charts.
- **Artist Insights:** Discover your followed and recently played artists, along with details about their top tracks and albums. Artist profiles include images and direct links to Spotify for further exploration.
- **Genre Visualization:** Visualize your top genres using interactive pie charts and bar graphs. This feature aggregates data from your top artists' genres, providing a clear picture of your music preferences.
- **User Profile:** Display your Spotify user profile details, including the currently playing track, recently played tracks, total listening time, and other relevant information.

## Technologies Used

- **Python Libraries:** Spotipy, Streamlit, Altair, Plotly, Pandas
- **Data Sources:** Spotify API for music data, Yahoo Finance API for stock data
- **Frontend:** HTML and CSS for custom styling to enhance user experience

## Installation

### Prerequisites
- Python 3.6 or higher
- Spotify Developer Account to get the necessary API credentials (Client ID and Client Secret)

### Steps
1. **Clone the repository**
   ```sh
   git clone https://github.com/DharaniIlango/Spotify_Analysis
   cd Spotify_Analysis
   ```
2. **Install the required dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up Spotify API credentials**
   -> Add your Spotify API credentials:
   ```sh
   SPOTIPY_CLIENT_ID='your_client_id'
   SPOTIPY_CLIENT_SECRET='your_client_secret'
   SPOTIPY_REDIRECT_URI='your_redirect_uri'
   ```
4. **Run the Streamlit application**
   ```sh
   streamlit run main.py
   ```
   
### Project Structure
```sh
Spotify_Analysis/
│
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .streamlit
│     └──config.toml        # Cofiguration File (included in the repo, needs to be initialized)
└── README.md               # Project documentation
```

## Contact
For any questions or suggestions, feel free to contact me at dharaniilango1209@gmail.com
