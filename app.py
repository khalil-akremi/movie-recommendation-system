import streamlit as st
import pickle
import requests

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api*************************************"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Load the data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# App title
st.header("🎬 Movie Recommender System")

# Display popular movies
st.subheader("🔥 Popular Movies")
popular_movie_ids = [
    1632, 299536, 17455, 2830, 429422,
    9722, 13972, 240, 155, 598,
    914, 255709, 572154
]
popular_posters = [fetch_poster(mid) for mid in popular_movie_ids]

# Show posters in columns
cols = st.columns(5)
for i, poster_url in enumerate(popular_posters):
    with cols[i % 5]:
        st.image(poster_url, use_container_width=True)


# Dropdown for movie selection
selectvalue = st.selectbox("🎥 Select a movie to get recommendations:", movies_list)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# Button to show recommendations
if st.button("🔍 Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)
    st.subheader("🎯 Recommended for you:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(movie_names[i])
            st.image(movie_posters[i], use_container_width=True)


