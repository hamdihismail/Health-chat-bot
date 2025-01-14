import requests

places_api = 'AIzaSyAhXIbqYmKSZaR4dB4nmBQ49pzUFek64E0'

def find_nearby(language,region,latitude,longitude,radius,service_type):


    data = {
    'languageCode': language,
    'regionCode': region,
    'includedTypes': service_type,
    'maxResultCount': 10,
    'locationRestriction': {
        'circle': {
            'center': {
                'latitude': latitude,
                'longitude': longitude
        },
        'radius': radius
        }
    }
    }
    url = 'https://places.googleapis.com/v1/places:searchNearby?key='+places_api
    try:
        response = requests.post(url, data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")

    return response.content