import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id, movie_title=None):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=db3a9d00dfac6fedb8bab8a078b16f87&language=en-US".format(
            movie_id)
        response = requests.get(url, timeout=10, verify=False)
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        pass

    # Title-based search fallback
    if movie_title:
        try:

            search_url = "https://api.themoviedb.org/3/search/movie?api_key=db3a9d00dfac6fedb8bab8a078b16f87&query={}".format(
                movie_title)
            response = requests.get(search_url, timeout=10, verify=False)
            search_data = response.json()

            if 'results' in search_data and len(search_data['results']) > 0:
                for movie in search_data['results']:
                    if movie.get('poster_path'):
                        return "https://image.tmdb.org/t/p/w500/" + movie['poster_path']
        except Exception as e:
            print(f"Search failed for {movie_title}: {e}")


    return "https://via.placeholder.com/500x750?text=Poster+Not+Available"
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)

        recommended_movies_posters.append(fetch_poster(movie_id, movie_title))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])