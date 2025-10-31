from dotenv import load_dotenv
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os
import requests

#############
# Functions #
#############

def find_half_of_day(hour):
  """
  Description: Finds half of day (AM or PM) and adjusts param `half` if needed (subtract 12 from 24 hour clock) \n
  Returns: hour (modified if needed)
  """
  half_of_day = None
  
  if (hour < 12):
    half_of_day = 'AM'
    if (hour == 0): hour = 12
  elif (hour == 12):
    half_of_day = 'PM'
  else:
    hour -= 12
    half_of_day = 'PM'

  return hour, half_of_day

#################
# Env Variables #
#################
load_dotenv()

API_KEY = os.getenv('API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')

##########################
# Open Weather API Stuff #
##########################

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

#####################
# One Call API Data #
#####################

one_call_api: str = f'https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,alerts&units={t_units}&lang={language}&appid={API_KEY}'
# https://openweathermap.org/api/one-call-3#parameter

sun_data = {
  'rise': None,
  'rise-half': None,
  'set': None,
  'set-half': None,
}
pressure_data = None
humidity_data = None
dew_point_data = None
uvi_data = None
cloud_data = None
visibility_data = {
  'distance': None,
  'symbol': '~',
}
wind_data = {
  'speed': None,
  'deg': None,
  'gust': None,
}

curr_weather_data = {
  'id': None,
  'forecast': None,
  'description': None,
  'temp': None,
  'icon': None,
  'alt-text': None
}

hourly_data = []
daily_data = []

r_one_call_data = requests.get(one_call_api)

if (r_one_call_data.status_code == 200):
  one_call_json = r_one_call_data.json()
  # print(one_call_json)

  # Current Weather
  curr_weather_data['id'] = one_call_json['current']['weather'][0]['id']
  curr_weather_data['forecast'] = one_call_json['current']['weather'][0]['main']
  curr_weather_data['description'] = (one_call_json['current']['weather'][0]['description']).capitalize()
  curr_weather_data['temp'] = round(one_call_json['current']['temp']) # [modifiable] Rounds value to no decimals by default, remove `round()` function to prevent rounding
  curr_weather_data['icon'] = one_call_json['current']['weather'][0]['icon']

  match curr_weather_data['icon']:
    case '01d': 
      curr_weather_data['alt-text'] = 'day time clear sky icon'
    case '02d':
      curr_weather_data['alt-text'] = 'day time few clouds icon'
    case '03d':
      curr_weather_data['alt-text'] = 'day time scattered clouds icons'
    case '04d':
      curr_weather_data['alt-text'] = 'day time break clouds icon'
    case '09d':
      curr_weather_data['alt-text'] = 'day time shower rain icon'
    case '10d':
      curr_weather_data['alt-text'] = 'day time rain icon'
    case '11d':
      curr_weather_data['alt-text'] = 'day time thunderstorm icon'
    case '13d':
      curr_weather_data['alt-text'] = 'day time snow icon'
    case '50d':
      curr_weather_data['alt-text'] = 'day time mist icon'
    case '01n':
      curr_weather_data['alt-text'] = 'night time clear sky icon'
    case '02n':
      curr_weather_data['alt-text'] = 'night time few clouds icon'
    case '03n':
      curr_weather_data['alt-text'] = 'night time scattered clouds icon'
    case '04n':
      curr_weather_data['alt-text'] = 'night time break clouds icon'
    case '09n':
      curr_weather_data['alt-text'] = 'night time shower rain icon'
    case '10n':
      curr_weather_data['alt-text'] = 'night time rain icon'
    case '11n':
      curr_weather_data['alt-text'] = 'night time thunderstorm icon'
    case '13n':
      curr_weather_data['alt-text'] = 'night time snow icon'
    case '50n':
      curr_weather_data['alt-text'] = 'night time mist icon'
    case _: 
      curr_weather_data['alt-text'] = 'no icon'

  # Sun Data
  sun_data['rise'] = one_call_json['current']['sunrise'] # Unix time stamp (Epoch time / Posix time)
  rise_dt = datetime.fromtimestamp(sun_data['rise'])
  rise_hour = rise_dt.hour
  rise_min = rise_dt.minute

  if (twelveHourTime):
    rise_hour, sun_data['rise-half'] = find_half_of_day(rise_hour)
    sun_data['rise'] = f'{rise_hour}:{rise_min:02d}'
  else:
    sun_data['rise'] = f'{rise_hour:02d}:{rise_min:02d}'


  sun_data["set"] = one_call_json['current']['sunset']
  set_dt = datetime.fromtimestamp(sun_data['set'])
  set_hour = set_dt.hour
  set_minute = set_dt.minute

  if (twelveHourTime):
    set_hour, sun_data['set-half'] = find_half_of_day(set_hour)
    sun_data['set'] = f'{set_hour}:{set_minute:02d}'
  else:
    sun_data['set'] = f'{set_hour:02d}:{set_minute:02d}'

  # Wind Speed
  wind_data['speed'] = round(one_call_json['current']['wind_speed'])
  wind_data['deg'] = one_call_json['current']['wind_deg']
  wind_data['gust'] = one_call_json['current']['wind_gust']

  # Humidity
  humidity_data = one_call_json['current']['humidity']

  # Visibility
  visibility_data['distance'] = round(one_call_json['current']['visibility'] * 0.001, 2)

  if (visibility_data['distance'] == 10.00):
    visibility_data['symbol'] = '>'

  # Pressure
  pressure_data = one_call_json['current']['pressure']

  # Ultra-Violet Index
  uvi_data = one_call_json['current']['uvi']

  # Dew Point Data
  dew_point_data = one_call_json['current']['dew_point']

  # Cloud Data
  cloud_data = one_call_json['current']['clouds']

  # Hourly Data
  for i in range(12):
    hourly_data.append(
      {
        'time': None,
        'half-of-day': None,
        'prob-of-precip': None,
        'temp': None,
        'rain-exists': False,
        'rain-vol': None,
        'rain-units': 'mm/h',
        'snow-exists': False,
        'snow-vol': None,
        'snow-units': 'mm/h',
      }
    )

    x = i + 1 # Index for json, 0 = current hour

    # Time
    hourly_data[i]['time'] = one_call_json['hourly'][x]['dt']
    hourly_time = datetime.fromtimestamp(hourly_data[i]['time'])
    hour = hourly_time.hour

    if (twelveHourTime):
      hour, hourly_data[i]['half-of-day'] = find_half_of_day(hour)
      hourly_data[i]['time'] = f'{hour}'
    else:
      hourly_data[i]['time'] = f'{hour:02d}'

    # Probability of Precipitation
    hourly_data[i]['prob-of-precip'] = one_call_json['hourly'][x]['pop']

    # Temp
    hourly_data[i]['temp'] = one_call_json['hourly'][x]['temp']

    # Rain & Snow Data
    try:
      hourly_data[i]['rain-vol'] = one_call_json['hourly'][x]['rain']['1h']

      if (hourly_data[i]['rain-vol'] != None): 
        hourly_data[i]['rain-exists'] = True
    except:
      # print('Could not find rain data')
      hourly_data[i]['rain-exists'] = False

    try:
      hourly_data[i]['snow-vol'] = one_call_json['hourly'][x]['snow']['1h']

      if (hourly_data[i]['snow-vol'] != None):
        hourly_data[i]['snow-exists'] = True
    except:
      hourly_data[i]['snow-exists'] = False


    if (t_units == 'imperial' and (hourly_data[i]['rain-exists'] or hourly_data[i]['snow-exists'])):
      mm_to_inch = 0.03937008 # 1mm = 0.03937008 inch
      
      if (hourly_data[i]['rain-exists']):
        hourly_data[i]['rain-vol'] *= mm_to_inch
        hourly_data[i]['rain-units'] = 'in/h'
      
      if (hourly_data[i]['snow-exists']):
        hourly_data[i]['snow-vol'] *= mm_to_inch
        hourly_data[i]['snow-units'] = 'in/h'


  # Daily Data
  for i in range(5):
    daily_data.append(
      {
        'date': None,

        'low-temp': None,
        'high-temp': None,

        'sun-rise-hour': None,
        'sun-rise-minute': None,
        'sun-rise-half-of-day': None,

        'sun-set-hour': None,
        'sun-set-minute': None,
        'sun-set-half-of-day': None,

        'moon-rise-hour': None,
        'moon-rise-minute': None,
        'moon-rise-half-of-day': None,

        'moon-set-hour': None,
        'moon-set-minute': None,
        'moon-set-half-of-day': None,

        'prob-of-precip': None,

        'rain-exists': False,
        'rain-vol': None,
        'rain-units': 'mm',

        'snow-exists': False,
        'snow-vol': None,
        'snow-units': 'mm',

        'icon': None,
        'alt-text': None,
      }
    )

    x = i + 1 # index for json, 0 = current day

    # Date
    daily_data['date'] = one_call_json['daily'][x]['dt']

    # Temp
    daily_data['low-temp'] = one_call_json['daily'][x]['temp']['min']
    daily_data['high-temp'] = one_call_json['daily'][x]['temp']['max']

    # Sun Rise

    # Sun Set

    # Moon Rise

    # Moon Set

    # Probability of Precipitation
    daily_data['prob-of-precip'] = one_call_json['daily'][x]['pop']

    # Rain & Snow

    # Icon & Alt text
    daily_data['icon'] = one_call_json['daily'][i]['weather']['icon']
    # TODO make icon alt text match case a function

else:
  print(f'Could not get One Call API data: {r_one_call_data.status_code}')

########################
# Air Quality Index Data
########################

air_quality_api: str = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}'
aqi_data = None

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

####################
# Geocoding API Data
####################

geocoding_api: str = f'http://api.openweathermap.org/geo/1.0/reverse?lat={LATITUDE}&lon={LONGITUDE}&limit=1&appid={API_KEY}'

location_data = {
  'name': None,
  'country': None,
  'state': None,
}

r_geocoding_data = requests.get(geocoding_api)

if (r_geocoding_data.status_code == 200):
  geocoding_json = r_geocoding_data.json()

  location_data["name"] = geocoding_json[0]['name']
  location_data["country"] = geocoding_json[0]['country']
  location_data["state"] = geocoding_json[0]['state']
else:
  print(f'Could not get Geocoding API data: {r_geocoding_data.status_code}')

#####################
# Jinja Environment #
#####################

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
  cw_icon = curr_weather_data['icon'],
  cw_icon_alt = curr_weather_data["alt-text"],
  curr_temp = curr_weather_data["temp"],
  curr_description = curr_weather_data['description'],

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
  visibility = visibility_data["distance"],
  vis_symbol = visibility_data["symbol"],

  # Pressure Data
  pressure = pressure_data,

  # Cloud Data
  cloud_coverage = cloud_data,

  # Dew Point Data
  dew_point = dew_point_data,

  # Ultra-Violet Index Data
  uvi = uvi_data,

  # Air Quality Index Data
  aqi = aqi_data

  # Hourly Data

  # Daily Data
)

with open("weather.html", "w") as html:
  html.write(output)

print('Process completed successfully')