import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=175c17cb7c76ff236c8af28466da9b26'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similaritry[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        recommended_movies.append((movies.iloc[i[0]].title))
        recommended_movies_posters.append((fetch_poster(movies.iloc[i[0]].movie_id)))
    return recommended_movies, recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similaritry=pickle.load(open('similaritry.pkl', 'rb'))

st.title('Movie Recommender System')

movie_selected = st.selectbox(
'Write movie name here',
movies['title'].values)

if st.button("Recommend movies"):
    names,posters=recommend(movie_selected)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])







