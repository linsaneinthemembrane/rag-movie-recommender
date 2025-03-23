import ollama
from config import ALL_GENRES_MAP
from typing import List, Dict, Any
import re
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def parse_letterboxd_profile(profile_url: str) -> List[Dict[str, Any]]:
    """Parse a Letterboxd profile URL to extract watched movies"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        movies = []
        # Find all movie entries
        movie_entries = soup.find_all('li', class_='poster-container')
        
        for entry in movie_entries:
            # Extract movie title
            title_elem = entry.find('div', class_='film-poster')
            if not title_elem:
                continue
                
            title = title_elem.get('data-target-link', '').strip('/').split('/')[-1].replace('-', ' ').title()
            
            # Extract rating if available
            rating_elem = entry.find('span', class_='rating')
            rating = None
            if rating_elem:
                rating_text = rating_elem.text.strip()
                # Convert star rating to number (e.g., "★★★★★" to 5.0)
                rating = len(rating_text) / 2
            
            # Extract year if available
            year_elem = entry.find('span', class_='year')
            year = None
            if year_elem:
                year = int(year_elem.text.strip('()'))
            
            movie = {
                'title': title,
                'year': year,
                'rating': rating,
                'genres': []  # We'll need to fetch genres from TMDB
            }
            movies.append(movie)
        
        return movies
    except Exception as e:
        st.error(f"Error parsing Letterboxd profile: {str(e)}")
        return []

def analyze_taste_profile(movies: List[Dict[str, Any]], max_movies: int = 50) -> str:
    """Analyze user's taste profile based on their movie preferences"""
    try:
        st.write(f"Starting analysis with {len(movies)} movies")  # Debug message
        
        # If we have more movies than max_movies, sample them
        if len(movies) > max_movies:
            movies = sorted(movies, key=lambda x: x.get('rating', 0) or 0, reverse=True)[:max_movies]
            st.write(f"Sampled down to {len(movies)} movies")  # Debug message
        
        # Get movie titles for analysis
        movie_titles = [m.get('title', '') for m in movies if m.get('title')]
        st.write(f"Prepared {len(movie_titles)} movie titles for analysis")  # Debug message
        
        # Generate taste profile using DeepSeek
        st.write("Calling DeepSeek model...")  # Debug message
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "You are a movie taste analyzer. Create a creative and engaging taste profile based on the user's preferences. First, write 3-4 sentences analyzing their movie preferences. Then, on a new line, write a creative three-word phrase that captures their taste (e.g., 'Mind-Bending Sci-Fi Thriller' or 'Emotional Action Drama'). Make the three words flow naturally together and avoid using commas. Do not use any special characters or formatting in your response."},
                {"role": "user", "content": f"Create a taste profile for someone who likes these movies: {', '.join(movie_titles)}. Be creative and engaging."}
            ]
        )
        st.write("Received response from DeepSeek")  # Debug message
        
        # Clean up any extra whitespace and special characters
        analysis = response["message"]["content"]
        analysis = re.sub(r'\s+', ' ', analysis).strip()
        analysis = re.sub(r'\*\*|\*|_|#', '', analysis)  # Remove markdown formatting
        
        # Split into main analysis and three-word phrase
        parts = analysis.split('\n')
        if len(parts) >= 2:
            main_analysis = parts[0].strip()
            three_word_phrase = parts[-1].strip()
            return f"{main_analysis}\n\n{three_word_phrase}"
        
        # If no newline found, try to split by last sentence
        sentences = analysis.split('.')
        if len(sentences) > 1:
            main_analysis = '. '.join(sentences[:-1]) + '.'
            three_word_phrase = sentences[-1].strip()
            return f"{main_analysis}\n\n{three_word_phrase}"
        
        return analysis
    except Exception as e:
        st.error(f"Error in analyze_taste_profile: {str(e)}")
        st.write(f"Full error details: {str(e)}")  # Debug message
        return f"Error generating taste profile: {str(e)}"

def generate_festival_theme(movies: List[Dict[str, Any]], mood: str = "balanced") -> str:
    """Generate a festival theme and description using DeepSeek"""
    try:
        mood_prompts = {
            "balanced": "Create a balanced festival theme that includes a mix of different genres and moods",
            "uplifting": "Create an uplifting festival theme focusing on feel-good and inspiring movies",
            "thoughtful": "Create a thoughtful festival theme focusing on deep, meaningful films",
            "thrilling": "Create an exciting festival theme focusing on action, suspense, and thrillers",
            "emotional": "Create an emotional festival theme focusing on dramas and character-driven stories"
        }
        
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "You are a film festival curator. Create an engaging festival theme and description based on the movies and the specified mood. Select exactly 4 movies that create a cohesive narrative journey. Format your response EXACTLY as follows:\n\nFestival Name: [name]\n\nDescription: [Write a compelling paragraph that explains how these 4 movies connect thematically and create a meaningful journey for the viewer. Focus on the emotional and intellectual progression from one film to the next.]\n\nViewing Order:\n1. [movie title]\n2. [movie title]\n3. [movie title]\n4. [movie title]\n\nDo not include any thinking process, notes, asterisks, or additional text. Do not use any markdown formatting. Keep the format clean and simple."},
                {"role": "user", "content": f"{mood_prompts.get(mood, mood_prompts['balanced'])} for these movies: {', '.join([m.get('title', '') for m in movies])}. Select exactly 4 movies that create a meaningful journey."}
            ]
        )
        
        # Clean up the response
        content = response["message"]["content"]
        # Remove any thinking process or notes
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        # Remove any lines that start with common thinking indicators
        content = '\n'.join(line for line in content.split('\n') 
                          if not any(line.strip().startswith(indicator) 
                                   for indicator in ['Hmm', 'Okay', 'Let me', 'Now,', 'Maybe', 'Perhaps']))
        # Remove all asterisks and leading/trailing spaces from each line
        content = '\n'.join(line.strip().replace('*', '') for line in content.split('\n'))
        # Clean up any extra newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    except Exception as e:
        return f"Error generating festival theme: {str(e)}"

def generate_directors_commentary(movie):
    """Generate AI-powered director's commentary for a movie"""
    try:
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "You are a film critic providing director's commentary. Analyze themes, cinematography, and storytelling elements."},
                {"role": "user", "content": f"Provide director's commentary for {movie.get('title', '')}. Focus on themes, cinematography, and storytelling elements."}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error generating commentary: {str(e)}"

def analyze_visual_style(movie):
    """Analyze and describe the visual style of a movie"""
    try:
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "You are a cinematography expert. Analyze and describe the visual style of movies."},
                {"role": "user", "content": f"Analyze the visual style of {movie.get('title', '')}. Focus on cinematography, color palette, and visual themes."}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error analyzing visual style: {str(e)}"

def get_analysis(movies: List[Dict[str, Any]], analysis_type: str) -> str:
    """Get analysis from DeepSeek model"""
    try:
        # Prepare the prompt based on analysis type
        if analysis_type == "taste":
            prompt = f"""Based on these movies: {', '.join(m['title'] for m in movies)}
            Provide a brief 5-sentence analysis of the viewer's taste in movies."""
        else:  # festival
            prompt = f"""Based on these movies: {', '.join(m['title'] for m in movies)}
            Suggest a 5-sentence theme for a personal film festival featuring these movies."""
        
        # Get response from DeepSeek
        response = ollama.chat(model='deepseek-coder:6.7b', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract the response and remove any think tags
        analysis = response['message']['content']
        analysis = re.sub(r'<think>.*?</think>', '', analysis, flags=re.DOTALL)
        
        # Limit to 5 sentences
        sentences = re.split(r'[.!?]+', analysis)
        sentences = [s.strip() for s in sentences if s.strip()]
        analysis = '. '.join(sentences[:5]) + '.'
        
        return analysis
    except Exception as e:
        st.error(f"Error getting analysis: {str(e)}")
        return "Unable to generate analysis at this time." 