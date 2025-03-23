# --- API KEYS ---
TMDB_API_KEY = "tmdb_key"
TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzViZjFkYTRkNzAyYzkxZjY3NDFjZGE1ZDk1ZDI2ZSIsIm5iZiI6MTc0MjIyMDQ0NS4wNTUsInN1YiI6IjY3ZDgyYzlkOTE2NWYzNzExODAxODViZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rUJHGrxbbK-wWFQp0Er-Of1eEShEBZ453oLsUWr5My8"

# --- Constants for Time-Based Features ---
TIME_OF_DAY = {
    "morning": (5, 12),
    "afternoon": (12, 17),
    "evening": (17, 22),
    "night": (22, 5)
}

SEASONS = {
    "spring": (3, 5),
    "summer": (6, 8),
    "fall": (9, 11),
    "winter": (12, 2)
}

# Genre mapping
GENRE_MAP = {
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
TV_GENRE_MAP = {
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
ALL_GENRES_MAP = {**GENRE_MAP, **TV_GENRE_MAP} 