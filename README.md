# Spotify Top Songs Analysis

## Project Description

The Spotify Analysis Dashboard is a robust application built using Python and Streamlit, designed to provide users with detailed insights into their Spotify usage and music preferences.

## Key Features

- **Behavioral Audio Analysis:** Map your listening habits using an interactive Audio Mood Quadrant based on track psychology (Valence vs. Energy).
- **Market Comparison:** Gain insights into Spotify's stock performance over time.
- **Artist Insights:** Discover your followed artists in a clean, responsive grid layout.
- **Data Caching:** Optimized API calls to prevent rate limiting and improve load times.

## Technologies Used

- **Python Libraries:** Spotipy, Streamlit, Altair, Plotly, Pandas, python-dotenv
- **Data Sources:** Spotify API for music data, Yahoo Finance API for stock data

## Local Installation (Linux / macOS)

### Prerequisites

- Python 3.8 or higher
- Spotify Developer Account to get the necessary API credentials (Client ID and Client Secret)

### Steps

1. **Clone the repository**
   ```sh
   git clone [https://github.com/DharaniIlango/Spotify_Analysis](https://github.com/DharaniIlango/Spotify_Analysis)
   cd Spotify_Analysis
   ```
2. **Create and Activate a Virtual Environment**
   ```sh
   python3 -m venv spotify_env
   source spotify_env/bin/activate
   ```
3. **Install the required dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up Environment Variables**
   Create a .env file in the root directory and add your keys:
   ```sh
   SPOTIFY_CLIENT_ID="your_client_id"
   SPOTIFY_CLIENT_SECRET="your_client_secret"
   SPOTIFY_REDIRECT_URI="http://localhost:8501/callback"
   ```
5. **Run the Streamlit App**

   ```sh
   streamlit run main.py
   ```

   > Developed by தரணி இளங்கோ.
