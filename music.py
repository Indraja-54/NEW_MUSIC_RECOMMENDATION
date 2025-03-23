import os
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import gdown

# Spotify API Credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize Spotify Client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to load pickle from Google Drive or local file
def load_or_download_pickle(url, output_filename):
    if not os.path.exists(output_filename):
        st.write(f"Downloading {output_filename} for the first time...")
        gdown.download(url, output_filename, quiet=False, fuzzy=True)
    with open(output_filename, "rb") as f:
        return pickle.load(f)

# Function to fetch album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Recommendation function
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:21]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Google Drive URLs (converted)
df_pkl_url = "https://drive.google.com/uc?export=download&id=108334Cg-i5knPIypAOb4u4zg6kmENQ6j"
similarity_pkl_url = "https://drive.google.com/uc?export=download&id=1voUY0VlPtwfOmtds20D_D9oFRBspQdJ4"

# Load pickles (only download if not available)
music = load_or_download_pickle(df_pkl_url, "music.pkl")
similarity = load_or_download_pickle(similarity_pkl_url, "similarity.pkl")

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: white;'>🎵 Spotify Music Recommender 🎵</h1>", unsafe_allow_html=True)

music_list = music['song'].values
selected_song = st.selectbox("🔍 Select a song for recommendations", music_list)

if st.button("🎧 Get Recommendations"):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    st.markdown(f"### 🎶 Now Playing: {selected_song}")
    st.image(get_song_album_cover_url(selected_song, music[music['song'] == selected_song].artist.values[0]), width=250)

    st.markdown("### 🎼 Recommended Songs")

    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        .song-card {
            text-align: center;
            animation: fadeIn 0.5s ease-in-out;
            transition: transform 0.3s ease-in-out;
        }
        .song-card:hover {
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    num_columns = 4
    rows = [recommended_music_names[i:i+num_columns] for i in range(0, len(recommended_music_names), num_columns)]
    poster_rows = [recommended_music_posters[i:i+num_columns] for i in range(0, len(recommended_music_posters), num_columns)]

    for row, poster_row in zip(rows, poster_rows):
        cols = st.columns(num_columns)
        for idx, col in enumerate(cols):
            if idx < len(row):
                with col:
                    st.markdown(f"<div class='song-card'>", unsafe_allow_html=True)
                    st.image(poster_row[idx], use_container_width=True)
                    st.markdown(f"**{row[idx]}**", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
