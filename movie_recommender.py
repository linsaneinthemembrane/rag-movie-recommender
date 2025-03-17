import streamlit as st
import requests
from datetime import datetime
import ollama

# --- API KEYS ---
TMDB_API_KEY = "tmdb_key"
TMDB_ACCESS_TOKEN = "tmdb_access_token"

# --- TMDB API Functions ---
def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params = {"query": query}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning(f"Error searching for movie: {response.text}")
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

def clean_and_shorten_response(response_text):
    # Remove the thinking part of response
    if "<think>" in response_text and "</think>" in response_text:
        start_idx = response_text.find("</think>") + len("</think>")
        response_text = response_text[start_idx:].strip()
    
    # Split into sentences (simple approach)
    sentences = response_text.replace("! ", ". ").replace("? ", ". ").split(". ")
    
    short_response = ". ".join(sentences[:3])
    if not short_response.endswith("."):
        short_response += "."
        
    return short_response

def extract_year(date_str):
    if not date_str:
        return "Unknown"
    try:
        return date_str.split("-")[0]
    except:
        return "Unknown"

# Genre mapping
genre_map = {
    28: "Action", 
    12: "Adventure",
    16: "Animation", 
    35: "Comedy", 
    80: "Crime",
    99: "Documentary", 
    18: "Drama", 
    10751: "Family",
    14: "Fantasy",
    36: "History", 
    27: "Horror", 
    10402: "Music",
    9648: "Mystery", 
    10749: "Romance", 
    878: "Sci-Fi",
    10770: "TV Movie", 
    53: "Thriller", 
    10752: "War",
    37: "Western"
}

# TV Genre mapping
tv_genre_map = {
    10759: "Action & Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    10762: "Kids",
    9648: "Mystery",
    10763: "News",
    10764: "Reality",
    10765: "Sci-Fi & Fantasy",
    10766: "Soap",
    10767: "Talk",
    10768: "War & Politics",
    37: "Western"
}

# Combine both genre maps
all_genres_map = {**genre_map, **tv_genre_map}

# Get genre names from genre IDs
def get_genre_names(genre_ids):
    return [all_genres_map.get(genre_id, "") for genre_id in genre_ids if genre_id in all_genres_map]

# Streamlit UI
st.title("🎬 Personalized Movie & TV Show Recommender")

user_input = st.text_area("Enter movies or TV shows you like (comma-separated)")

genres = sorted(list(set(all_genres_map.values())))
selected_genres = st.multiselect("Select preferred genres", genres)

start_year, end_year = st.slider("Select release year range", 1900, 2023, (1990, 2023))

# Add rating slider starting at 8.0
min_rating = st.slider("Minimum rating", 0.0, 10.0, 8.0, 0.1)

if st.button("Get Recommendations"):
    if not user_input:
        st.warning("Please enter at least one movie or TV show.")
    else:
        user_titles = [title.strip() for title in user_input.split(",")]
        
        all_recommendations = []
        
        for title in user_titles:
            movie_results = search_movies(title)
            tv_results = search_tv(title)
            
            # Get similar content for the first result of each type
            if movie_results:
                movie_id = movie_results[0].get("id")
                similar_movies = get_similar_movies(movie_id)
                all_recommendations.extend(similar_movies)
                
            if tv_results:
                tv_id = tv_results[0].get("id")
                similar_tv = get_similar_tv(tv_id)
                all_recommendations.extend(similar_tv)
        
        # Filter recommendations based on user preferences
        filtered_recommendations = []
        
        for rec in all_recommendations:
            # Get release year
            release_year = None
            if "release_date" in rec and rec["release_date"]:
                release_year = extract_year(rec["release_date"])
            elif "first_air_date" in rec and rec["first_air_date"]:
                release_year = extract_year(rec["first_air_date"])
            
            # Check if it meets the criteria
            if release_year and release_year != "Unknown":
                try:
                    release_year_int = int(release_year)
                    rating = rec.get("vote_average", 0)
                    
                    if rating >= min_rating and start_year <= release_year_int <= end_year:
                        # Check genres
                        rec_genre_ids = rec.get("genre_ids", [])
                        rec_genres = get_genre_names(rec_genre_ids)
                        
                        if not selected_genres or any(genre in rec_genres for genre in selected_genres):
                            filtered_recommendations.append(rec)
                except ValueError:
                    continue
        
        # Remove duplicates based on ID
        unique_recommendations = []
        seen_ids = set()
        
        for rec in filtered_recommendations:
            if rec["id"] not in seen_ids:
                seen_ids.add(rec["id"])
                unique_recommendations.append(rec)
        
        # Sort by rating
        sorted_recommendations = sorted(unique_recommendations, key=lambda x: x.get("vote_average", 0), reverse=True)
        
        if sorted_recommendations:
            # Display recommendations in a 2-column grid
            for i in range(0, min(len(sorted_recommendations), 6), 2):
                # Create two columns for each row of recommendations
                col1, col2 = st.columns(2)
                
                # First column
                with col1:
                    if i < len(sorted_recommendations):
                        rec = sorted_recommendations[i]
                        title = rec.get("title", rec.get("name", "Unknown Title"))
                        
                        st.subheader(title)
                        
                        # Display poster
                        poster_path = rec.get("poster_path")
                        if poster_path:
                            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", caption=title, width=200)
                        
                        # Display metadata
                        release_year = extract_year(rec.get("release_date", rec.get("first_air_date", "")))
                        st.write(f"Release Year: {release_year}")
                        st.write(f"Rating: {rec.get('vote_average', 0):.1f}/10")
                        
                        # Display genres
                        genre_ids = rec.get("genre_ids", [])
                        genres = get_genre_names(genre_ids)
                        if genres:
                            st.write(f"Genres: {', '.join(genres)}")
                        
                        # Get LLM summary using DeepSeek R1
                        try:
                            response = ollama.chat(
                                model="deepseek-r1",
                                messages=[
                                    {"role": "system", "content": "You are a movie recommendation assistant. Provide concise summaries in 3 sentences or less without any thinking process."},
                                    {"role": "user", "content": f"In 3 sentences or less, summarize why '{title}' is a good recommendation for someone who likes {', '.join(user_titles)}. Be brief and direct."}
                                ]
                            )
                            raw_summary = response["message"]["content"]
                            summary = clean_and_shorten_response(raw_summary)
                            st.write(summary)
                        except Exception as e:
                            st.write(f"Error generating summary: {str(e)}")
                
                # Second column
                with col2:
                    if i + 1 < len(sorted_recommendations):
                        rec = sorted_recommendations[i + 1]
                        title = rec.get("title", rec.get("name", "Unknown Title"))
                        
                        st.subheader(title)
                        
                        # Display poster
                        poster_path = rec.get("poster_path")
                        if poster_path:
                            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", caption=title, width=200)
                        
                        # Display metadata
                        release_year = extract_year(rec.get("release_date", rec.get("first_air_date", "")))
                        st.write(f"Release Year: {release_year}")
                        st.write(f"Rating: {rec.get('vote_average', 0):.1f}/10")
                        
                        # Display genres
                        genre_ids = rec.get("genre_ids", [])
                        genres = get_genre_names(genre_ids)
                        if genres:
                            st.write(f"Genres: {', '.join(genres)}")
                        
                        # Get LLM summary using DeepSeek
                        try:
                            response = ollama.chat(
                                model="deepseek-r1",
                                messages=[
                                    {"role": "system", "content": "You are a movie recommendation assistant. Provide concise summaries in 3 sentences or less without any thinking process."},
                                    {"role": "user", "content": f"In 3 sentences or less, summarize why '{title}' is a good recommendation for someone who likes {', '.join(user_titles)}. Be brief and direct."}
                                ]
                            )
                            raw_summary = response["message"]["content"]
                            summary = clean_and_shorten_response(raw_summary)
                            st.write(summary)
                        except Exception as e:
                            st.write(f"Error generating summary: {str(e)}")
        else:
            st.error("No recommendations found. Try adjusting your preferences or entering different movies or TV shows.")

# Add a section for trending movies and shows
st.subheader("Trending Movies and TV Shows")

try:
    trending_movies = get_popular_movies()
    trending_tv = get_popular_tv()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Trending Movies")
        for movie in trending_movies[:5]:
            title = movie.get("title", "Unknown")
            year = extract_year(movie.get("release_date", ""))
            rating = movie.get("vote_average", 0)
            st.write(f"{title} ({year}) - Rating: {rating:.1f}/10")
    
    with col2:
        st.write("Trending TV Shows")
        for show in trending_tv[:5]:
            name = show.get("name", "Unknown")
            year = extract_year(show.get("first_air_date", ""))
            rating = show.get("vote_average", 0)
            st.write(f"{name} ({year}) - Rating: {rating:.1f}/10")
except Exception as e:
    st.error(f"Error loading trending content: {str(e)}")

st.markdown("---")
st.write("Data provided by The Movie Database (TMDb)")
st.write("Powered by DeepSeek R1 for personalized recommendations")
