import requests
import datetime
from tavily import TavilyClient
import os
from math import *
from crewai import Crew
from agents import Agents
from utils import *
from tasks import Tasks
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools. gmail.search import GmailSearch
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)


credentials = get_gmail_credentials(
    token_file="token.json",
    scopes= ["https://mail.google.com/"],
    client_secrets_file="credentials.json"
)
api_resource = build_resource_service(credentials=credentials)

def filter_emails_tool():
  filter_agent = Agents.email_filter_agent()
  search = GmailSearch(api_resource=api_resource)
  emails = search("in:inbox")
  mails = []
  for email in emails:
    mails.append(
        {
          "id": email["id"],
          "threadId": email ["threadId"],
          "snippet": email["snippet"],
          "sender": email["sender"],
        }
  )
    
  filter_task = Tasks.filter_emails_task(agent=filter_agent, emails=mails)
  crew = Crew(
      agents=[filter_agent],
      tasks=[filter_task],
      verbose=2
  )
  result= crew.kickoff()
  print('CREW RESULT',result)
  return result

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

def calculator_tool(operation:str)-> str:
  """
  Performs a specified mathematical operation
  like sum, minus, multiplication, division, etc.
  The input to this tool should be a mathematical
  expression, a couple examples are `200*7` or `5000/2*10`
  """
  try:
    print('Performaing operation: ', operation)
    output = eval(operation)
    return f"The result of the operation is {output}"
  except SyntaxError:
    return "Error: Invalid syntax in mathematical expression"