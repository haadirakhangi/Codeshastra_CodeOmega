import requests
import datetime
from tavily import TavilyClient
import os


def weather_tool(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""

    print('Fetching weather information...')
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")
    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']

    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]

    return f'The current temperature is {current_temperature}°C'

def search_tool(query: str) -> str:
  """Get information about anything from the internet"""
  print('Searching information from the web...')
  tavily_client = TavilyClient(api_key = os.environ["TAVILY_API_KEY"])
  response = tavily_client.get_search_context(query= query, search_depth="advanced", max_tokens = 4000)
  return response