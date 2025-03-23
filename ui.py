import streamlit as st
from config import ALL_GENRES_MAP
from api import (
    search_movies, search_tv, get_similar_movies, get_similar_tv,
    get_popular_movies, get_popular_tv, get_movie_details,
    get_recommendations
)
from utils import (
    get_current_time_context, calculate_runtime, format_runtime,
    extract_year, get_genre_names
)
from analysis import (
    analyze_taste_profile, generate_festival_theme,
    generate_directors_commentary, analyze_visual_style,
    parse_letterboxd_profile
)

def display_movie_recommendations():
    """Display the movie recommendations interface"""
    st.header("🎬 Get Personalized Movie Recommendations")
    
    # Add Letterboxd profile input
    letterboxd_url = st.text_input("Enter your Letterboxd profile URL (optional)", "", key="letterboxd_url_recommendations")
    if letterboxd_url:
        with st.spinner("Fetching your Letterboxd profile..."):
            watched_movies = parse_letterboxd_profile(letterboxd_url)
            if watched_movies:
                st.success(f"Successfully loaded {len(watched_movies)} movies from your Letterboxd profile!")
            else:
                st.error("Could not load movies from your Letterboxd profile. Please check the URL and try again.")
    
    # Get user preferences
    st.subheader("Your Preferences")
    user_preferences = st.text_area(
        "What kind of movies do you like? (e.g., action, drama, sci-fi)",
        height=100,
        key="user_preferences"
    )
    
    # Genre selection
    st.write("Select your preferred genres:")
    selected_genres = []
    cols = st.columns(3)
    for i, (genre_id, genre_name) in enumerate(ALL_GENRES_MAP.items()):
        with cols[i % 3]:
            if st.checkbox(genre_name, key=f"genre_{genre_id}_recommendations"):
                selected_genres.append(genre_id)
    
    # Get recommendations
    if st.button("Get Recommendations", key="get_recommendations_btn"):
        with st.spinner("Finding the perfect movies for you..."):
            recommendations = get_recommendations(
                user_preferences,
                selected_genres,
                watched_movies if letterboxd_url else None
            )
            display_recommendations(recommendations)

def display_festival_generator():
    """Display the personal film festival generator interface"""
    st.header("🎭 Create Your Personal Film Festival")
    
    # Add Letterboxd profile input
    letterboxd_url = st.text_input("Enter your Letterboxd profile URL (optional)", "", key="letterboxd_url_festival")
    if letterboxd_url:
        with st.spinner("Fetching your Letterboxd profile..."):
            watched_movies = parse_letterboxd_profile(letterboxd_url)
            if watched_movies:
                st.success(f"Successfully loaded {len(watched_movies)} movies from your Letterboxd profile!")
            else:
                st.error("Could not load movies from your Letterboxd profile. Please check the URL and try again.")
    
    # Festival mood selection
    st.subheader("Festival Mood")
    mood = st.selectbox(
        "Choose the mood for your festival",
        ["balanced", "uplifting", "thoughtful", "thrilling", "emotional"],
        format_func=lambda x: x.title(),
        key="festival_mood"
    )
    
    # Generate festival
    if st.button("Generate Festival", key="generate_festival_btn"):
        with st.spinner("Creating your perfect film festival..."):
            festival = generate_festival_theme(
                watched_movies if letterboxd_url else [],
                mood
            )
            
            # Split the festival response into sections
            sections = festival.split('\n\n')
            
            # Display festival name and description
            if len(sections) >= 2:
                festival_name = sections[0].replace('Festival Name:', '').strip()
                description = sections[1].replace('Description:', '').strip()
                
                # Clean up any remaining asterisks, quotes, and extra spaces
                festival_name = festival_name.replace('*', '').replace('"', '').strip()
                
                st.header(f"🎬 {festival_name}")
                st.write(description)
                
                # Display viewing order with posters
                if len(sections) >= 3:
                    st.subheader("📅 Viewing Order")
                    viewing_order = sections[2].replace('Viewing Order:', '').strip()
                    
                    # Parse the viewing order
                    movie_titles = []
                    movie_descriptions = []
                    for line in viewing_order.split('\n'):
                        if line.strip():
                            # Extract movie title and description (assuming format: "1. Movie Title - Description")
                            if ' - ' in line:
                                # Split by the first occurrence of ' - '
                                title_part, description = line.split(' - ', 1)
                                # Remove the number if present
                                title = title_part.split('. ', 1)[1].strip() if '. ' in title_part else title_part.strip()
                            else:
                                title = line.split('. ', 1)[1].strip() if '. ' in line else line.strip()
                                description = ""
                            movie_titles.append(title)
                            movie_descriptions.append(description)
                    
                    # Create a row of movie posters
                    cols = st.columns(4)
                    
                    for i, (title, description) in enumerate(zip(movie_titles[:4], movie_descriptions[:4])):  # Limit to 4 movies
                        with cols[i]:
                            try:
                                # Search for the movie
                                results = search_movies(title)
                                if results and len(results) > 0:
                                    movie = results[0]  # Get the first result
                                    if movie and movie.get('id'):
                                        # Get detailed movie information including runtime
                                        movie_details = get_movie_details(movie['id'])
                                        if movie_details:
                                            # Display movie poster
                                            poster_path = movie_details.get("poster_path")
                                            if poster_path:
                                                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                                                st.image(poster_url, width=150)
                                            
                                            # Display movie title
                                            st.markdown(f"**{title}**")
                                            
                                            # Display description if available
                                            if description:
                                                st.markdown(f"_{description}_")
                                            
                                            # Display runtime
                                            runtime = movie_details.get('runtime')
                                            if runtime:
                                                st.write(f"Runtime: {format_runtime(runtime)}")
                                            
                                            # Display rating
                                            vote_average = movie_details.get('vote_average')
                                            if vote_average:
                                                st.write(f"Rating: {vote_average:.1f}/10")
                                else:
                                    st.write(title)  # Fallback if movie not found
                            except Exception as e:
                                st.error(f"Error displaying movie {title}: {str(e)}")
                                st.write(title)  # Fallback if there's an error

def display_taste_analysis():
    """Display taste analysis section"""
    st.header("🎯 Your Taste Profile")
    
    # Initialize session state for analysis
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'movies_list' not in st.session_state:
        st.session_state.movies_list = []
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Letterboxd Profile", "CSV Upload", "Manual Input"])
    
    with tab1:
        st.write("Enter your Letterboxd profile URL:")
        profile_url = st.text_input("Letterboxd Profile URL", placeholder="https://letterboxd.com/username/films/", key="letterboxd_url_analysis")
        if profile_url:
            if st.button("Import from Letterboxd", key="import_letterboxd_btn"):
                with st.spinner("Fetching your Letterboxd profile..."):
                    st.session_state.movies_list = parse_letterboxd_profile(profile_url)
                    if st.session_state.movies_list:
                        st.success(f"Successfully imported {len(st.session_state.movies_list)} movies from your Letterboxd profile!")
                    else:
                        st.error("No movies were found in your profile. Please check the URL and try again.")
    
    with tab2:
        st.write("Upload your Letterboxd CSV export:")
        uploaded_file = st.file_uploader("Upload Letterboxd CSV", type=['csv'], key="csv_uploader")
        if uploaded_file is not None:
            with open("temp_letterboxd.csv", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.session_state.movies_list = parse_letterboxd_profile("temp_letterboxd.csv")
            if st.session_state.movies_list:
                st.success(f"Successfully imported {len(st.session_state.movies_list)} movies from your CSV!")
            else:
                st.error("No movies were found in your CSV file. Please check the file format and try again.")
    
    with tab3:
        st.write("Or enter your favorite movies manually:")
        favorite_movies = st.text_area("Enter your favorite movies (comma-separated)", key="manual_movies_input")
        if favorite_movies:
            st.session_state.movies_list = [{"title": title.strip(), "genres": []} for title in favorite_movies.split(",") if title.strip()]
            if st.session_state.movies_list:
                st.success(f"Successfully added {len(st.session_state.movies_list)} movies!")
    
    if st.session_state.movies_list:
        # Display stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Movies", len(st.session_state.movies_list))
        with col2:
            avg_rating = sum(m.get('rating', 0) or 0 for m in st.session_state.movies_list) / len(st.session_state.movies_list)
            st.metric("Average Rating", f"{avg_rating:.1f}/5")
        
        # Show sample of imported movies
        st.subheader("Sample of Imported Movies")
        sample_movies = st.session_state.movies_list[:5]
        for movie in sample_movies:
            st.write(f"- {movie.get('title', 'Unknown')} ({movie.get('year', 'N/A')})")
        
        # Analysis button and results
        if st.button("Analyze My Taste", key="analyze_taste_btn"):
            st.write("Starting analysis...")  # Debug message
            try:
                with st.spinner("Analyzing your taste profile..."):
                    st.write("Calling analyze_taste_profile...")  # Debug message
                    st.session_state.analysis_result = analyze_taste_profile(st.session_state.movies_list)
                    st.write("Analysis complete!")  # Debug message
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.write(f"Full error details: {str(e)}")  # Debug message
        
        # Display analysis result if available
        if st.session_state.analysis_result:
            st.subheader("🎭 Your Movie Taste Profile")
            
            # Split the analysis into main text and three-word phrase
            parts = st.session_state.analysis_result.split('\n\n')
            if len(parts) == 2:
                main_analysis, three_word_phrase = parts
                # Display the three-word phrase prominently
                st.markdown(f"**{three_word_phrase}**")
                st.markdown("---")
                # Display the main analysis
                st.write(main_analysis)
            else:
                st.write(st.session_state.analysis_result)

def display_trending_content():
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