import requests
import streamlit as st
import ollama
from config import TMDB_ACCESS_TOKEN
from typing import List, Optional, Dict, Any

def search_movies(query: str):
    """Search for movies using TMDB API"""
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        headers = {
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
            "accept": "application/json"
        }
        params = {
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": 1
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        st.error(f"Error searching movies: {str(e)}")
        return []

def search_tv(query):
    url = "https://api.themoviedb.org/3/search/tv"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params = {"query": query}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error searching for TV show: {response.text}")
        return []

def get_similar_movies(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error getting similar movies: {response.text}")
        return []

def get_similar_tv(tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/similar"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error getting similar TV shows: {response.text}")
        return []

def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error getting popular movies: {response.text}")
        return []

def get_popular_tv():
    url = "https://api.themoviedb.org/3/tv/popular"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error getting popular TV shows: {response.text}")
        return []

def get_movie_details(movie_id: int):
    """Get detailed information about a movie using TMDB API"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except Exception as e:
        st.error(f"Error getting movie details: {str(e)}")
        return None

def get_movie_credits(movie_id):
    """Get movie credits including cinematographer and composer"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_recommendations(user_preferences: str, selected_genres: List[int], watched_movies: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Get personalized movie recommendations based on user preferences and watched movies"""
    try:
        # Get recommendations from DeepSeek
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "You are a movie recommendation expert. Based on the user's preferences and watched movies, suggest new movies they might enjoy. Focus on finding movies that match their taste profile, even if they don't match all genres exactly."},
                {"role": "user", "content": f"User preferences: {user_preferences}\nWatched movies: {', '.join([m.get('title', '') for m in (watched_movies or [])])}\nPreferred genres: {', '.join([ALL_GENRES_MAP.get(g, '') for g in selected_genres])}"}
            ]
        )
        
        # Parse recommendations
        recommendations = []
        for title in response["message"]["content"].split('\n'):
            if title.strip():
                # Search for the movie
                results = search_movies(title.strip())
                if results:
                    movie_id = results[0].get("id")
                    details = get_movie_details(movie_id)
                    if details:
                        # Check if it matches at least one preferred genre
                        if not selected_genres or any(genre_id in details.get("genre_ids", []) for genre_id in selected_genres):
                            recommendations.append(details)
        
        return recommendations[:6]  # Return top 6 recommendations
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return [] 