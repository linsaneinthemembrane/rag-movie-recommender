# RAG Movie Recommender App

## Overview

This project is a personalized movie and TV show recommendation application built with Streamlit. The app allows users to discover new content based on their preferences, leveraging the TMDB (The Movie Database) API for data and DeepSeek R1 for generating personalized recommendation summaries.

## Features

- **Personalized Recommendations**: Get movie and TV show recommendations based on titles you already enjoy
- **Genre Filtering**: Filter recommendations by preferred genres
- **Year Range Selection**: Discover content from specific time periods
- **Rating Threshold**: Set minimum rating requirements for recommendations
- **Trending Content**: View currently popular movies and TV shows
- **AI-Generated Summaries**: Each recommendation includes a concise explanation of why it matches your preferences

## Technologies Used

### Core Technologies
- **Python**: Primary programming language
- **Streamlit**: Web application framework for creating the user interface
- **TMDB API**: Source of movie and TV show data, including metadata and recommendations

### AI Integration
- **DeepSeek R1**: Open-source large language model used to generate personalized recommendation summaries
- **Ollama**: Local AI model serving platform that hosts the DeepSeek R1 model

### Additional Libraries
- **Requests**: HTTP library for making API calls to TMDB
- **Datetime**: For handling date information

## Learning Objectives

This project demonstrates how to:

1. Build an interactive web application using Streamlit
2. Integrate with external APIs (TMDB) to fetch and process data
3. Implement filtering and sorting algorithms for personalized recommendations
4. Incorporate local AI capabilities using Ollama and DeepSeek R1
5. Create a responsive UI with a grid layout for displaying recommendations
6. Handle API errors and edge cases gracefully
7. Process and clean AI-generated text for consistent presentation

## Setup and Installation

1. Clone the repository
2. Install the required dependencies:
```
pip install streamlit requests ollama
```
3. Install Ollama from [ollama.com](https://ollama.com)
4. Pull the DeepSeek R1 model:
```
ollama pull deepseek-r1
```
5. Set up your TMDB API credentials (API key and access token)
6. Run the application:
```
streamlit run movie_recommender.py
```

## Usage

1. Enter one or more movies or TV shows you enjoy (comma-separated)
2. Select your preferred genres (optional)
3. Adjust the release year range and minimum rating
4. Click "Get Recommendations" to see personalized suggestions
5. Explore trending movies and TV shows in the section below

## Future Enhancements

- Mood-based recommendations
- Film festival explorer
- Visual style matching
- User accounts and saved preferences
- Social sharing capabilities

## Acknowledgments

- Data provided by [The Movie Database (TMDB)](https://www.themoviedb.org/)
- Recommendation summaries powered by DeepSeek R1

