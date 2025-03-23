import streamlit as st
from ui import (
    display_movie_recommendations,
    display_festival_generator,
    display_taste_analysis
)

def main():
    st.title("🎬 Movie Recommender")
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["Movie Recommendations", "Personal Film Festival", "Taste Analysis"])
    
    with tab1:
        display_movie_recommendations()
    
    with tab2:
        display_festival_generator()
    
    with tab3:
        display_taste_analysis()
    
    # Footer
    st.markdown("---")
    st.markdown("Data provided by [The Movie Database (TMDb)](https://www.themoviedb.org/)")
    st.text("Powered by DeepSeek R1 for personalized recommendations")

if __name__ == "__main__":
    main() 