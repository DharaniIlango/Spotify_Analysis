# Spotify Top Songs Analysis

## Project Description
Spotify Top Songs Analysis is a web application that leverages the Spotify API to provide users with insights into their listening history. The application categorizes users' top songs into short, medium, and long-term periods and displays various audio features such as danceability, energy, and valence.

## Features
- **Top Songs Analysis**: View your most-played songs over short, medium, and long-term periods.
- **Audio Features Insights**: Explore detailed audio features of your top tracks, including danceability, energy, and valence.
- **User-Friendly Interface**: Interact with a clean and intuitive interface built with Streamlit.

## Technologies Used
- **Pandas**: For data manipulation and analysis.
- **Streamlit**: To create a web application interface.
- **Spotipy**: A Python library for the Spotify Web API.

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
2. **Create a virtual environment and activate it**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install the required dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up Spotify API credentials**
   -> Create a .env file in the project root directory.
   -> Add your Spotify API credentials:
   ```sh
   SPOTIPY_CLIENT_ID='your_client_id'
   SPOTIPY_CLIENT_SECRET='your_client_secret'
   SPOTIPY_REDIRECT_URI='your_redirect_uri'
   ```
5. **Run the Streamlit application**
   ```sh
   streamlit run Top_Songs_Analysis.py
   ```
   
### Project Structure
```sh
Spotify_Analysis/
│
├── Top_Songs_Analysis.py   # Main application file
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (included in the repo, needs to be initialized)
└── README.md               # Project documentation
```

## Contact
For any questions or suggestions, feel free to contact me at dharaniilango1209@gmail.com
