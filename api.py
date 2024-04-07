import streamlit as st
import pickle
import pandas as pd
import requests
import json
def fetch_poster(movie_id):
    response = requests.get('https://www.omdbapi.com/?i={}&apikey=e1538323'.format(movie_id))
    try:
        data = response.json()
        if response.status_code == 200:
            if 'Poster' in data:
                return data['Poster']
            else:
                print("Poster not found in the response data:", data)
                return None
        else:
            print("Error fetching data from OMDB API. Status code:", response.status_code)
            return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON response from OMDB API:", e)
        return None



def recommend(movie, movies, similarity):
    movie_index = movies[movies['movie_name'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].movie_name)
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]]['movie_id']))
    return recommended_movies, recommended_movies_posters

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.read_pickle('movies.pkl')

movies_list = movies['movie_name'].values
st.title('Movie Recommender System')

selected_movie_name = st.sidebar.selectbox(
    'How would you like to choose?',
    movies_list)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name, movies, similarity)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(5):
        with eval(f'col{i+1}'):
            st.text(recommendations[i])
            st.image(posters[i])
