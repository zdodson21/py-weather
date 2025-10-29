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

# Open Weather API Stuff

temp_units = ['standard', 'metric', 'imperial']
units = temp_units[2] # [modifiable] Change this index value if you wish to use different temperature units (Imperial default)

supported_langs = [
  "sq", # 0: Albanian
  "af", # 1: Afrikaans
  "ar", # 2: Arabic
  "az", # 3: Azerbaijani
  "eu", # 4: Basque
  "be", # 5: Belarusian
  "bg", # 6: Bulgarian
  "ca", # 7: Catalan
  "zh_cn", # 8: Chinese Simplified
  "zh_tw", # 9: Chinese Traditional
  "hr", # 10: Croatian
  "cz", # 11: Czech
  "da", # 12: Danish
  "nl", # 13: Dutch
  "en", # 14: English
  "fi", # 15: Finnish
  "fr", # 16: French
  "gl", # 17: Galician
  "de", # 18: German
  "el", # 19: Greek
  "he", # 20: Hebrew
  "hi", # 21: Hindi
  "hu", # 22: Hungarian
  "is", # 23: Icelandic
  "id", # 24: Indonesian
  "it", # 25: Italian
  "ja", # 26: Japanese
  "kr", # 27: Korean
  "ku", # 28: Kurmanji (Kurdish)
  "la", # 29: Latvian
  "lt", # 30: Lithuanian
  "mk", # 31: Macedonian
  "no", # 32: Norwegian
  "fa", # 33: Persian (Farsi)
  "pl", # 34: Polish
  "pt", # 35: Portuguese
  "pt_br", # 36: Português Brasil
  "ro", # 37: Romanian
  "ru", # 38: Russian
  "sr", # 39: Serbian
  "sk", # 40: Slovak
  "sl", # 41: Slovenian
  "sp", # 42: Spanish
  "se", # 43: Swedish
  "th", # 44: Thai
  "tr", # 45: Turkish
  "uk", # 46: Ukranian
  "vi", # 47: Vietnamese
  "zu", # 48: Zulu
]
language = supported_langs[14] # [modifiable] Change the index value if you wish to use a different language (English default)

one_call_api = f'https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely&units={units}&lang={language}&appid={API_KEY}'
air_quality_api = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}'
geocoding_api = f'http://api.openweathermap.org/geo/1.0/reverse?lat={LATITUDE}&lon={LONGITUDE}&limit=1&appid={API_KEY}'

sun = {
  'rise': None,
  'set': None,
}
curr_temp = None
pressure = None
humidity = None
dew_point = None
uvi = None
clouds = None
visibility = None
wind = {
  'speed': None,
  'deg': None,
  'gust': None,
}

curr_weather = {
  'id': None,
  'forecast': None,
  'description': None,
  'icon': None,
}
hourly = []
daily = []

air_quality_index = None

location = {
  'name': None,
  'country': None,
  'state': None,
}

r_one_call_data = requests.get(one_call_api)
if (r_one_call_data.status_code == 200):
  one_call_json = r_one_call_data.json()
else:
  print(f'Could not get One Call API data: {r_one_call_data.status_code}')

r_air_quality_data = requests.get(air_quality_api)
if (r_air_quality_data == 200):
  air_quality_json = r_air_quality_data.json()
else:
  print(f'Could not get Air Quality API data: {r_air_quality_data.status_code}')

r_geocoding_data = requests.get(geocoding_api)
if (r_geocoding_data == 200):
  geocoding_json = r_geocoding_data.json()
else:
  print(f'Could not get Geocoding API data: {r_geocoding_data.status_code}')

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
