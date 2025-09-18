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
    headers = {"User-Agent": "my-app/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.status_code, resp.text
    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} → {e}")
    except requests.ConnectionError:
        print("Connection error: unable to reach the server.")
    except requests.Timeout:
        print("Request timed out.")
    except requests.RequestException as e:
        print(f"Unexpected error: {e}")
    return None, ""

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

    movies = []
    
    if isinstance(imdb_data, tuple):
        status_code, html_text = imdb_data
        if status_code != 200:
            return []
    else:
        html_text = imdb_data
        
    soup = BeautifulSoup(html_text, "html.parser")
    
    script_tag = soup.select_one('script[type="application/ld+json"]')
    if not script_tag:
        return movies
    
    
    try:
        payload = json.loads(script_tag.get_text(strip=True))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return movies
    

    items = payload.get("itemListElement", []) if isinstance(payload, dict) else []

    for el in items:
        info = (el or {}).get("item", {}) or {}
        rating = (info.get("aggregateRating") or {}).get("ratingValue", 0.0)
        movies.append({
            "Title": info.get("name", "N/A"),
            "Description": info.get("description", "No description available"),
            "Rating": rating,
        })

    return movies
    

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
    auth_bytes = f"{client_id}:{client_secret}".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        'Authorization': f'Basic {auth_base64}',
        #'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    try:
        resp = requests.post(auth_url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        return resp.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error retrieving Spotify token: {e}")
        return ""

# 4% credit    
def spotify_search_params(client_id, client_secret, **kwargs):
    """
    Construct url, headers and params. Reference API docs (link above) to use the arguments
    """
    
    access_token = access_spotify(client_id, client_secret)
    # What is the url endpoint for search?
    url = 'https://api.spotify.com/v1/search'
    # How is Authentication performed? Hint: use access_token from function of access_spotify
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # SPACES in url is problematic. How should you handle queries with field filters?
    query_parts = []
    for key, value in kwargs.items():
        if key in ['artist', 'track', 'album', 'year', 'genre', 'label']:
            query_parts.append(f"{key}:{value}")
            
    query = ' '.join(query_parts)
    # Include keyword arguments in params dictionary
    params = {
        'q': query,
        'type': kwargs.get('type', 'track'),  
        'limit': kwargs.get('limit', 20),    
        'offset': kwargs.get('offset', 0)     
    }
    
    params = {k: v for k, v in params.items() if v is not None}
    
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
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
    

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
    num_pages = math.ceil(total / limit)
    
    # Generate requests for each page
    all_requests = [
        spotify_search_params(
            client_id,
            client_secret,
            artist=artist_name,
            type="track",
            limit=limit,
            offset=page * limit,
        )
        for page in range(num_pages)
    ]

    return all_requests


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
    results = []
    for url, headers, url_params in tracks_request:
        try:
            resp = api_get_request(url, headers, url_params)
        except Exception as e:
            print(e)
            continue

        if resp and isinstance(resp, dict):
            tracks = resp.get("tracks", {})
            items = tracks.get("items", [])
            if isinstance(items, list):
                results.extend(items)

        time.sleep(0.2)

    return results

# 4% credit
def parse_api_response(data):
    """
    Parse Spotify API results to extract cover images URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    parsed = json.loads(data)
    items = parsed.get("tracks", {}).get("items", [])

    # Collect all "url" fields from album images
    urls = [
        img["url"]
        for item in items
        for img in item.get("album", {}).get("images", [])
        if "url" in img
    ]

    return urls


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
    for container in review_containers:
        author = container.find("span", class_="display-name-link")
        rating = container.find("span", class_="rating-other-user-rating")
        date = container.find("span", class_="review-date")
        text = container.find("div", class_="text")

        reviews_list.append({
            "Author": author.get_text(strip=True) if author else None,
            "Rating": float(rating.find("span").get_text(strip=True)) if rating and rating.find("span") else None,
            "Date": date.get_text(strip=True) if date else None,
            "Review": text.get_text(strip=True) if text else None
        })
        
    return reviews_list
