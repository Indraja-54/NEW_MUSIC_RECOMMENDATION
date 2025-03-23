import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize Spotify Client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to fetch album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image

# Recommendation function
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:21]:  # Get 20 recommendations
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: white;'>🎵 Spotify Music Recommender 🎵</h1>", unsafe_allow_html=True)

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_song = st.selectbox("🔍 Select a song for recommendations", music_list)

if st.button("🎧 Get Recommendations"):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    # Display Selected Song
    st.markdown(f"### 🎶 Now Playing: {selected_song}")
    st.image(get_song_album_cover_url(selected_song, music[music['song'] == selected_song].artist.values[0]), width=250)

    st.markdown("### 🎼 Recommended Songs")

    # Apply custom CSS for animation
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

    # Display recommendations in a **4-column grid**
    num_columns = 4
    rows = [recommended_music_names[i:i+num_columns] for i in range(0, len(recommended_music_names), num_columns)]
    poster_rows = [recommended_music_posters[i:i+num_columns] for i in range(0, len(recommended_music_posters), num_columns)]

    for row, poster_row in zip(rows, poster_rows):
        cols = st.columns(num_columns)  # Create 4 columns per row
        for idx, col in enumerate(cols):
            if idx < len(row):
                with col:
                    st.markdown(f"<div class='song-card'>", unsafe_allow_html=True)
                    st.image(poster_row[idx], use_container_width=True)
                    st.markdown(f"**{row[idx]}**", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
