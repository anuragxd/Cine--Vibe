import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def get_watch_providers(movie_id):
    """
    Fetches streaming providers for a specific movie ID in India (IN).
    Change 'IN' to 'US' if you want American streaming links.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    
    providers = []
    
    if response.status_code == 200:
        results = response.json().get('results', {})
        # 'IN' is the country code for India. Change to 'US' for USA.
        in_providers = results.get('IN', {}) 
        
        # 'flatrate' means subscription services like Netflix/Prime
        # 'rent' would be for rental services like Apple TV
        flatrate = in_providers.get('flatrate', [])
        
        for p in flatrate:
            providers.append(p['provider_name'])
            
    return providers[:3] # Return top 3 providers to keep UI clean

def search_movie_details(movie_name: str):
    """Searches for a movie and returns details + streaming info."""
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            movie = results[0]
            movie_id = movie['id']
            
            # Fetch the streaming info using our new function
            streaming_on = get_watch_providers(movie_id)
            
            return {
                "title": movie['title'],
                "overview": movie['overview'],
                "rating": movie['vote_average'],
                "release_date": movie['release_date'],
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                "streaming_on": streaming_on  # New Field!
            }
    return None