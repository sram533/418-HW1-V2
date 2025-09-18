import io, time, json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

import base64

# 2% credit
def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    
    [YOUR CODE HERE]

#3% credit
def parse_imdb(imdb_data):
    """
    Return the movie lists from imdb top chart URL.

    Args:
        raw_html (string): 

    Returns:
        movies (list): the list of movies with Title, Description and Rating.
    
        Example:
        movies = [
        {
            'Title': 'The Shawshank Redemption',
            'Description': 'A Maine banker convicted of the murder of his wife and her lover...',
            'Rating': 9.3,
        },
        {
            'Title': 'The Godfather',
            'Description': 'Don Vito Corleone, head of a mafia family, decides to hand over his empire...',
            'Rating': 9.2,

        },
            # ... more
        ]

    
    """

    [YOUR CODE HERE]

# 1% credit
def read_api_key(filepath):
    """
    Read the Spotify API Keys from file.
    
    Args:
        filepath (string): File containing API Keys
    Returns:
        client_id (string): Your client id
        client_secret (string): Your client secret
    """
    
    # feel free to modify this function if you are storing the API Key differently
    with open(filepath, 'r') as file:
        return json.load(file)


# 2% credit
def access_spotify(client_id, client_secret):
    """
    Authenticates the user and retrieves the bearer token required for API requests.
    """
    # 
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = [YOUR CODE HERE]

    headers = {
        'Authorization': f'Basic {auth_header}',
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = [YOUR CODE HERE]
    access_token = [YOUR CODE HERE]
    
    return access_token

# 4% credit    
def spotify_search_params(client_id, client_secret, **kwargs):
    """
    Construct url, headers and params. Reference API docs (link above) to use the arguments
    """
    # What is the url endpoint for search?
    url = [YOUR CODE HERE]
    # How is Authentication performed? Hint: use access_token from function of access_spotify
    headers = [YOUR CODE HERE]
    # SPACES in url is problematic. How should you handle queries with field filters?
    query = [YOUR CODE HERE]
    # Include keyword arguments in params dictionary
    params = [YOUR CODE HERE]
    
    return url, headers, params


# 2% credit
def api_get_request(url, headers, params):
    """
    Send a HTTP GET request and return a json response 
    
    Args:
        url (string): API endpoint url
        headers (dict): A python dictionary containing HTTP headers including Authentication to be sent
        url_params (dict): The parameters (required and optional) supported by endpoint
        
    Returns:
        results (json): response as json
    """
    # See requests.request?
    response = [YOUR CODE HERE]
    return [YOUR CODE HERE]
    

def spotify_search(client_id, client_secret, **kwargs):
    """
    Make an authenticated request to the Spotify API and return search results.

    Args:
        client_id (string): Your Spotify Client ID for Authentication
        client_secret (string): Your Spotify Client Secret for Authentication
        **kwargs: Additional search parameters (e.g., artist, track, album, etc.)

    Returns:
        total (integer): Total number of tracks matching the query
        tracks (list): List of dicts representing each track with name, and popularity
    """
    url, headers, params = spotify_search_params(client_id, client_secret, **kwargs)
    response_json = api_get_request(url, headers, params)
    total = response_json['tracks']['total']
    tracks = []
    if response_json['tracks']['items']:
            popularities = []
            for track in response_json['tracks']['items']:
                track_info = {
                    'track_name': track['name'],
                    'popularity': track['popularity']
                }
                tracks.append(track_info)
                popularities.append(track['popularity'])
            
    return total, tracks

# 4% credit
def paginated_spotify_search_requests(client_id, client_secret, artist_name, total,limit):
    """
    Returns a list of tuples (url, headers, params) for paginated search of all restaurants
    Args:
        client_id, client_secret (string): Your Spotify API Key for Authentication
        artist_name (string): Artist name
        total (int): Total number of items to be fetched
        limit (int): Number of items to fetch per request (default is 50)
    Returns:
        results (list): list of tuple (url, headers, params)
    """
    # HINT: Use total, offset and limit for pagination
    # You can reuse function location_search_params(...)
    [YOUR CODE HERE]


# 3% credit
def get_tracks(client_id, client_secret, artist_name):
    """
    Construct the pagination requests for ALL tracks by Given Artist on Spotify.

    Args:
        client_id (string): Your Spotify Client ID for Authentication
        client_secret (string): Your Spotify Client Secret for Authentication
        artist_name (string): Artist name

    Returns:
        results (list): List of dicts representing each track
    """
    total_items = 200
    limit = 50
    
    tracks_request = paginated_spotify_search_requests(api_key, location, total_items,limit)
    
    # Use returned list of (url, headers, url_params) and function api_get_request to retrive all restaurants
    # REMEMBER to pause slightly after each request.
    [YOUR CODE HERE]

# 4% credit
def parse_api_response(data):
    """
    Parse Spotify API results to extract cover images URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    [YOUR CODE HERE]


def html_fetcher(url):
    """
    Return the raw HTML at the specified URL.
    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    html_file = url_lookup.get(url)
    with open(html_file, 'rb') as file:
        html_text = file.read()
        return 200, html_text

# 11% credit
def parse_page(html):
    """
    Parse reviews from an IMDb movie reviews page.

    Args:
        html (string): HTML content of the IMDb reviews page.

    Returns:
        reviews (list): A list of dictionaries, each containing the review's rating, author, date, and content.
    """
    soup = BeautifulSoup(html,'html.parser')
    reviews_list = []

    # Find all review containers on the page
    review_containers = soup.find_all('div', class_='lister-item-content')
    # HINT: print reviews to see what http tag to extract
    [YOUR CODE HERE]
        
    return reviews_list
