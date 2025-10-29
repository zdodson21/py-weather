from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import os
import requests

# Env Variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')

# Open Weather API Stuff
temp_units = ['standard', 'metric', 'imperial']
t_units = temp_units[2] # [modifiable] Change this index value if you wish to use different temperature units (Imperial default)
disp_temp_units = None

match t_units:
  case 'standard': disp_temp_units = 'K'
  case 'metric': disp_temp_units = 'C'
  case 'imperial': disp_temp_units = 'F'
  case _: disp_temp_units = 'K'

speed_units = ['standard', 'imperial']
s_units = speed_units[1]

match s_units:
  case 'standard': s_units = 'm/s'
  case 'imperial': s_units = 'mph'
  case _: s_units = 'm/s'

twelveHourTime = True # [modifiable] Change to false to use a 24 hour clock

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

one_call_api: str = f'https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely&units={t_units}&lang={language}&appid={API_KEY}'
air_quality_api: str = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}'
geocoding_api: str = f'http://api.openweathermap.org/geo/1.0/reverse?lat={LATITUDE}&lon={LONGITUDE}&limit=1&appid={API_KEY}'

sun_data = {
  'rise': None,
  'set': None,
  'rise-half': None,
  'set-half': None,
}
curr_temp: float = None
pressure_data: float = None
humidity_data: float = None
dew_point_data: float = None
uvi_data: float = None
cloud_data: float = None
visibility_data: float = None
wind_data = {
  'speed': None,
  'deg': None,
  'gust': None,
}

curr_weather_data = {
  'id': None,
  'forecast': None,
  'description': None,
  'icon': None,
}
hourly_data = []
daily_data = []

aqi_data: float = None

location_data = {
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
if (r_air_quality_data.status_code == 200):
  air_quality_json = r_air_quality_data.json()

  aqi_data = air_quality_json['list'][0]['main']['aqi']
  
  match aqi_data:
    case 1: aqi_data = 'Good'
    case 2: aqi_data = 'Fair'
    case 3: aqi_data = 'Moderate'
    case 4: aqi_data = 'Poor'
    case 5: aqi_data = 'Very Poor'
    case _: aqi_data = 'ERROR'
else:
  print(f'Could not get Air Quality API data: {r_air_quality_data.status_code}')


r_geocoding_data = requests.get(geocoding_api)
if (r_geocoding_data.status_code == 200):
  geocoding_json = r_geocoding_data.json()

  location_data["name"] = geocoding_json[0]['name']
  location_data["country"] = geocoding_json[0]['country']
  location_data["state"] = geocoding_json[0]['state']
else:
  print(f'Could not get Geocoding API data: {r_geocoding_data.status_code}')


# Jinja Environment
env = Environment(loader = FileSystemLoader('./'))
template = env.get_template('template.html')

output = template.render(
  # Selected Units
  temp_unit = disp_temp_units,
  speed_unit = s_units,

  # Location Data
  location_name = location_data["name"],
  location_state = location_data["state"],
  
  # Current Weather Data
  cw_icon = '',
  cw_icon_alt = '',
  curr_temp = '',
  curr_description = '',

  # Sun Data
  use_half_of_day = twelveHourTime,
  sun_rise_time = sun_data["rise"],
  sun_rise_half_of_day = sun_data["rise-half"],

  sun_set_time = sun_data["set"],
  sun_set_half_of_day = sun_data["set-half"],
  
  # Wind Speed Data
  wind_speed = wind_data["speed"],
  wind_deg = wind_data["deg"],
  wind_gust = wind_data["gust"],

  # Humidity Data
  humidity = humidity_data,

  # Visibility Data
  visibiliy = visibility_data,

  # Pressure Data
  pressure = pressure_data,

  # Ultra-Violet Index Data
  uvi = uvi_data,

  # Air Quality Index Data
  aqi = aqi_data

  # Hourly Data

  # Daily Data
)

# Output populated template
with open("weather.html", "w") as html:
  html.write(output)
