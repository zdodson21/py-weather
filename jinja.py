from jinja2 import Environment, FileSystemLoader
import requests
import os
from dotenv import load_dotenv

# ! Ensure this is set to `False` before using in production environment
developer_mode = True

# Env Variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')

if (developer_mode):
  print(f'API Key: {API_KEY}')
  print(f'Latitude Coordinate: {LATITUDE}')
  print(f'Longitude Coordinate: {LONGITUDE}')

# Jinja Environment
env = Environment(loader = FileSystemLoader('./'))
template = env.get_template('template.html') # Change to template.html.j2 when done

output = template.render(
  name = 'Test',
  test2 = 'Test2',
)

# Output populated template
with open("weather.html", "w") as html:
  html.write(output)

# print(output)