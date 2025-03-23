from datetime import datetime
from config import TIME_OF_DAY, SEASONS, ALL_GENRES_MAP

def get_current_time_context():
    """Get current time context for recommendations"""
    current_time = datetime.now()
    current_hour = current_time.hour
    
    # Determine time of day
    for period, (start, end) in TIME_OF_DAY.items():
        if start <= current_hour < end:
            time_of_day = period
            break
    else:
        time_of_day = "night"
    
    # Determine season
    current_month = current_time.month
    for season, (start, end) in SEASONS.items():
        if start <= current_month <= end:
            current_season = season
            break
    else:
        current_season = "winter"
    
    return time_of_day, current_season

def calculate_runtime(movies):
    """Calculate total runtime for a list of movies"""
    total_minutes = 0
    for movie in movies:
        runtime = movie.get("runtime", 0)
        if runtime:
            total_minutes += runtime
    return total_minutes

def format_runtime(minutes):
    """Format runtime in minutes to hours and minutes"""
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"

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

def get_genre_names(genre_ids):
    return [ALL_GENRES_MAP.get(genre_id, "") for genre_id in genre_ids if genre_id in ALL_GENRES_MAP] 