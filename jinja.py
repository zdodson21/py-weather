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
        if (hour == 0):
            hour = 12
    elif (hour == 12):
        half_of_day = 'PM'
    else:
        hour -= 12
        half_of_day = 'PM'

    return hour, half_of_day


def set_alt_text(icon):
    """
    Description: returns alt text based on provided icon code
    """
    
    alt_text = ''

    match icon:
        case '01d':
            alt_text = 'day time clear sky icon'
        case '02d':
            alt_text = 'day time few clouds icon'
        case '03d':
            alt_text = 'day time scattered clouds icons'
        case '04d':
            alt_text = 'day time break clouds icon'
        case '09d':
            alt_text = 'day time shower rain icon'
        case '10d':
            alt_text = 'day time rain icon'
        case '11d':
            alt_text = 'day time thunderstorm icon'
        case '13d':
            alt_text = 'day time snow icon'
        case '50d':
            alt_text = 'day time mist icon'
        case '01n':
            alt_text = 'night time clear sky icon'
        case '02n':
            alt_text = 'night time few clouds icon'
        case '03n':
            alt_text = 'night time scattered clouds icon'
        case '04n':
            alt_text = 'night time break clouds icon'
        case '09n':
            alt_text = 'night time shower rain icon'
        case '10n':
            alt_text = 'night time rain icon'
        case '11n':
            alt_text = 'night time thunderstorm icon'
        case '13n':
            alt_text = 'night time snow icon'
        case '50n':
            alt_text = 'night time mist icon'
        case _:
            alt_text = f'no icon available for code: {icon}'

    return alt_text


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

temp_units = ['standard', 'metric', 'imperial'] # Kelvin, Celcius, Fahrenheit
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

twelveHourTime = True  # [modifiable] Change to false to use a 24 hour clock

supported_langs = [
    "sq",  # 0: Albanian
    "af",  # 1: Afrikaans
    "ar",  # 2: Arabic
    "az",  # 3: Azerbaijani
    "eu",  # 4: Basque
    "be",  # 5: Belarusian
    "bg",  # 6: Bulgarian
    "ca",  # 7: Catalan
    "zh_cn",  # 8: Chinese Simplified
    "zh_tw",  # 9: Chinese Traditional
    "hr",  # 10: Croatian
    "cz",  # 11: Czech
    "da",  # 12: Danish
    "nl",  # 13: Dutch
    "en",  # 14: English
    "fi",  # 15: Finnish
    "fr",  # 16: French
    "gl",  # 17: Galician
    "de",  # 18: German
    "el",  # 19: Greek
    "he",  # 20: Hebrew
    "hi",  # 21: Hindi
    "hu",  # 22: Hungarian
    "is",  # 23: Icelandic
    "id",  # 24: Indonesian
    "it",  # 25: Italian
    "ja",  # 26: Japanese
    "kr",  # 27: Korean
    "ku",  # 28: Kurmanji (Kurdish)
    "la",  # 29: Latvian
    "lt",  # 30: Lithuanian
    "mk",  # 31: Macedonian
    "no",  # 32: Norwegian
    "fa",  # 33: Persian (Farsi)
    "pl",  # 34: Polish
    "pt",  # 35: Portuguese
    "pt_br",  # 36: Português Brasil
    "ro",  # 37: Romanian
    "ru",  # 38: Russian
    "sr",  # 39: Serbian
    "sk",  # 40: Slovak
    "sl",  # 41: Slovenian
    "sp",  # 42: Spanish
    "se",  # 43: Swedish
    "th",  # 44: Thai
    "tr",  # 45: Turkish
    "uk",  # 46: Ukranian
    "vi",  # 47: Vietnamese
    "zu",  # 48: Zulu
]
language = supported_langs[14] # [modifiable] Change the index value if you wish to use a different language (English default)

mm_to_inch = 0.03937008  # 1mm = 0.03937008 inch

dev_mode = False

#####################
# One Call API Data #
#####################

one_call_api: str = f'https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,alerts&units={t_units}&lang={language}&appid={API_KEY}'
# https://openweathermap.org/api/one-call-3#parameter

sun_data = {
    'rise': None,
    'rise_half': None,
    'rise_exists': False,

    'set': None,
    'set_half': None,
    'set_exists': False,
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
    'alt_text': None
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
    curr_weather_data['temp'] = round(one_call_json['current']['temp'])
    curr_weather_data['icon'] = one_call_json['current']['weather'][0]['icon']
    curr_weather_data['alt_text'] = set_alt_text(curr_weather_data['icon'])

    # Sun Data
    try:
        # Unix time stamp (Epoch time / Posix time)
        sun_data['rise'] = one_call_json['current']['sunrise']

        if (sun_data['rise'] != None):
            sun_data['rise_exists'] = True
            rise_dt = datetime.fromtimestamp(sun_data['rise'])
            rise_hour = rise_dt.hour
            rise_min = rise_dt.minute

            if (twelveHourTime):
                rise_hour, sun_data['rise_half'] = find_half_of_day(rise_hour)
                sun_data['rise'] = f'{rise_hour}:{rise_min:02d}'
            else:
                sun_data['rise'] = f'{rise_hour:02d}:{rise_min:02d}'
    except:
        if (dev_mode):
            print('Could not find sun rise for current weather')

    try:
        sun_data["set"] = one_call_json['current']['sunset']

        if (sun_data['set'] != None):
            sun_data['set_exists'] = True
            set_dt = datetime.fromtimestamp(sun_data['set'])
            set_hour = set_dt.hour
            set_minute = set_dt.minute

            if (twelveHourTime):
                set_hour, sun_data['set_half'] = find_half_of_day(set_hour)
                sun_data['set'] = f'{set_hour}:{set_minute:02d}'
            else:
                sun_data['set'] = f'{set_hour:02d}:{set_minute:02d}'
    except:
        if (dev_mode):
            print('Could not find sun set for current weather')

    # Wind Speed
    wind_data['speed'] = round(one_call_json['current']['wind_speed'])
    wind_data['deg'] = one_call_json['current']['wind_deg']
    
    if (wind_data['deg'] <= 23 or wind_data['deg'] > 338):
        wind_data['deg'] = 'n'

    elif (wind_data['deg'] > 23 and wind_data['deg'] <= 68):
        wind_data['deg'] = 'ne'

    elif (wind_data['deg'] > 68 and wind_data['deg'] <= 113):
        wind_data['deg'] = 'e'

    elif (wind_data['deg'] > 113 and wind_data['deg'] <= 158):
        wind_data['deg'] = 'se'

    elif (wind_data['deg'] > 158 and wind_data['deg'] <= 203):
        wind_data['deg'] = 's'

    elif (wind_data['deg'] > 203 and wind_data['deg'] <= 248):
        wind_data['deg'] = 'sw'

    elif (wind_data['deg'] > 248 and wind_data['deg'] <= 293):
        wind_data['deg'] = 'w'

    elif (wind_data['deg'] > 293 and wind_data['deg'] <= 338):
        wind_data['deg'] = 'nw'

    wind_data['gust'] = one_call_json['current']['wind_gust']

    # Humidity
    humidity_data = one_call_json['current']['humidity']

    # Visibility
    visibility_data['distance'] = round(
        one_call_json['current']['visibility'] * 0.001, 2)

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
                'index': i,
                'time': None,
                'half_of_day': None,
                'prob_of_precip': None,
                'temp': None,
                'rain_exists': False,
                'rain_vol': None,
                'rain_units': 'mm/h',
                'snow_exists': False,
                'snow_vol': None,
                'snow_units': 'mm/h',
            }
        )

        x = i + 1  # Index for json, 0 = current hour

        # Time
        hourly_data[i]['time'] = one_call_json['hourly'][x]['dt']
        hourly_time = datetime.fromtimestamp(hourly_data[i]['time'])
        hour = hourly_time.hour

        if (twelveHourTime):
            hour, hourly_data[i]['half_of_day'] = find_half_of_day(hour)
            hourly_data[i]['time'] = f'{hour}'
        else:
            hourly_data[i]['time'] = f'{hour:02d}'

        # Probability of Precipitation
        hourly_data[i]['prob_of_precip'] = one_call_json['hourly'][x]['pop']

        # Temp
        hourly_data[i]['temp'] = one_call_json['hourly'][x]['temp']

        # Rain & Snow Data
        try:
            hourly_data[i]['rain_vol'] = one_call_json['hourly'][x]['rain']['1h']

            if (hourly_data[i]['rain_vol'] != None):
                hourly_data[i]['rain_exists'] = True
        except:
            # print('Could not find rain data')
            if (dev_mode):
                print(
                    f'No hourly rain data for json index: {x} | array index: {i}')

        try:
            hourly_data[i]['snow_vol'] = one_call_json['hourly'][x]['snow']['1h']

            if (hourly_data[i]['snow_vol'] != None):
                hourly_data[i]['snow_exists'] = True
        except:
            if (dev_mode):
                print(
                    f'No hourly snow data for json index: {x} | array index: {i}')

        if (t_units == 'imperial' and (hourly_data[i]['rain_exists'] or hourly_data[i]['snow_exists'])):
            if (hourly_data[i]['rain_exists']):
                hourly_data[i]['rain_vol'] *= mm_to_inch
                hourly_data[i]['rain_units'] = 'in/h'

            if (hourly_data[i]['snow_exists']):
                hourly_data[i]['snow_vol'] *= mm_to_inch
                hourly_data[i]['snow_units'] = 'in/h'

    # Daily Data
    for i in range(5):
        daily_data.append(
            {
                'index': i,
                
                'date': None,

                'low_temp': None,
                'high_temp': None,

                'sun_rise': None,
                'sun_rise_half_of_day': None,
                'sun_rise_exists': False,

                'sun_set': None,
                'sun_set_half_of_day': None,
                'sun_set_exists': False,

                'moon_rise': None,
                'moon_rise_half_of_day': None,
                'moon_rise_exists': False,

                'moon_set': None,
                'moon_set_half_of_day': None,
                'moon_set_exists': False,

                'prob_of_precip': None,

                'rain_exists': False,
                'rain_vol': None,
                'rain_units': 'mm.',

                'snow_exists': False,
                'snow_vol': None,
                'snow_units': 'mm.',

                'icon': None,
                'alt_text': None,
            }
        )

        x = i + 1  # index for json, 0 = current day

        # Date
        daily_data[i]['date'] = one_call_json['daily'][x]['dt']
        daily_date_dt = datetime.fromtimestamp(daily_data[i]['date'])
        daily_month = daily_date_dt.month

        match daily_month:
            case 1:
                daily_month = 'January'
            case 2:
                daily_month = 'February'
            case 3:
                daily_month = 'March'
            case 4:
                daily_month = 'April'
            case 5:
                daily_month = 'May'
            case 6:
                daily_month = 'June'
            case 7:
                daily_month = 'July'
            case 8:
                daily_month = 'August'
            case 9:
                daily_month = 'September'
            case 10:
                daily_month = 'October'
            case 11:
                daily_month = 'November'
            case 12:
                daily_month = 'December'

        daily_day = daily_date_dt.day

        daily_date = daily_date_dt.isoweekday()

        match daily_date:
            case 1:
                daily_date = 'Monday'
            case 2:
                daily_date = 'Tuesday'
            case 3:
                daily_date = 'Wednesday'
            case 4:
                daily_date = 'Thursday'
            case 5:
                daily_date = 'Friday'
            case 6:
                daily_date = 'Saturday'
            case 7:
                daily_date = 'Sunday'

        daily_data[i]['date'] = f'{daily_date}, {daily_month} {daily_day}'

        # Temp
        daily_data[i]['low_temp'] = one_call_json['daily'][x]['temp']['min']
        daily_data[i]['low_temp'] = round(daily_data[i]['low_temp'])

        daily_data[i]['high_temp'] = one_call_json['daily'][x]['temp']['max']
        daily_data[i]['high_temp'] = round(daily_data[i]['high_temp'])

        # Sun Rise
        try:
            daily_data[i]['sun_rise'] = one_call_json['daily'][x]['sunrise']

            if (daily_data[i]['sun_rise'] != None):
                daily_data[i]['sun_rise_exists'] = True
                daily_dt_s_rise = datetime.fromtimestamp(daily_data[i]['sun_rise'])
                daily_srh = daily_dt_s_rise.hour
                daily_srm = daily_dt_s_rise.minute

                if (twelveHourTime):
                    daily_srh, daily_data[i]['sun_rise_half_of_day'] = find_half_of_day(daily_srh)
                    daily_data[i]['sun_rise'] = f'{daily_srh}:{daily_srm:02d}'
                else:
                    daily_data[i]['sun_rise'] = f'{daily_srh:02d}:{daily_srm:02d}'
        except:
            if (dev_mode):
                print('cannot find daily sun rise')

        # Sun Set
        try:
            daily_data[i]['sun_set'] = one_call_json['daily'][i]['sunset']
            
            if (daily_data[i]['sun_set'] != None):
                daily_data[i]['sun_set_exists'] = True
                daily_dt_s_set = datetime.fromtimestamp(daily_data[i]['sun_set'])
                daily_ssh = daily_dt_s_set.hour
                daily_ssm = daily_dt_s_set.minute

                if (twelveHourTime):
                    daily_ssh, daily_data[i]['sun_set_half_of_day'] = find_half_of_day(daily_ssh)
                    daily_data[i]['sun_set'] = f'{daily_ssh}:{daily_ssm:02d}'
                else:
                    daily_data[i]['sun_set'] = f'{daily_ssh:02d}:{daily_ssm:02d}'
        except:
            if (dev_mode):
                print('Cannot find daily sun set')

        # Moon Rise
        try:
            daily_data[i]['moon_rise'] = one_call_json['daily'][i]['moonrise']

            if (daily_data[i]['moon_rise'] != None):
                daily_data[i]['moon_rise_exists'] = True
                daily_dt_m_rise = datetime.fromtimestamp(daily_data[i]['moon_rise'])
                daily_mrh = daily_dt_m_rise.hour
                daily_mrm = daily_dt_m_rise.minute

                if (twelveHourTime):
                    daily_mrh, daily_data[i]['moon_rise_half_of_day'] = find_half_of_day(daily_mrh)
                    daily_data[i]['moon_rise'] = f'{daily_mrh}:{daily_mrh:02d}'
                else:
                    daily_data[i]['moon_rise'] = f'{daily_mrh:02d}:{daily_mrh:02d}'
        except:
            if (dev_mode):
                print('Cannot find daily moon rise')

        # Moon Set
        try:
            daily_data[i]['moon_set'] = one_call_json['daily'][i]['moonset']

            if (daily_data[i]['moon_set']):
                daily_data[i]['moon_set_exists'] = True
                daily_dt_m_set = datetime.fromtimestamp(daily_data[i]['moon_set'])
                daily_msh = daily_dt_m_set.hour
                daily_msm = daily_dt_m_set.minute

                if (twelveHourTime):
                    daily_msh, daily_data[i]['moon_set_half_of_day'] = find_half_of_day(daily_msh)
                    daily_data[i]['moon_set'] = f'{daily_msh}:{daily_msh:02d}'
                else:
                    daily_data[i]['moon_set'] = f'{daily_msh:02d}:{daily_msh:02d}'
        except:
            if (dev_mode):
                print('Cannot find daily moon set')

        # Probability of Precipitation
        daily_data[i]['prob_of_precip'] = one_call_json['daily'][x]['pop']
        daily_data[i]['prob_of_precip'] = round(daily_data[i]['prob_of_precip'] * 100)

        # Rain & Snow
        try:
            daily_data[i]['rain_vol'] = one_call_json['daily'][x]['rain']

            if (daily_data[i]['rain_vol'] != None):
                daily_data[i]['rain_exists'] = True
        except:
            if (dev_mode):
                print(f'No daily rain data for json index: {x} | array index: {i}')

        try:
            daily_data[i]['snow_vol'] = one_call_json['daily'][x]['snow']

            if (daily_data[i]['snow_vol'] != None):
                daily_data[i]['snow_exists'] = True
        except:
            if (dev_mode):
                print(f'No daily snow data for json index: {x} | array index: {i}')

        if (t_units == 'imperial' and (daily_data[i]['rain_exists'] or daily_data[i]['snow_exists'])):
            if (daily_data[i]['rain_exists']):
                daily_data[i]['rain_vol'] *= mm_to_inch
                daily_data[i]['rain_vol'] = round(daily_data[i]['rain_vol'], 2)
                daily_data[i]['rain_units'] = 'in.'

            if (daily_data[i]['snow_exists']):
                daily_data[i]['snow_vol'] *= mm_to_inch
                daily_data[i]['snow_vol'] = round(daily_data[i]['snow_vol'], 2)
                daily_data[i]['snow_units'] = 'in.'

        # Icon & Alt text
        daily_data[i]['icon'] = one_call_json['daily'][x]['weather'][0]['icon']
        daily_data[i]['alt_icon'] = set_alt_text(daily_data[i]['icon'])

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
    print(
        f'Could not get Air Quality API data: {r_air_quality_data.status_code}')

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

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('template.html')

output = template.render(
    # Selected Units
    temp_unit = disp_temp_units,
    speed_unit = s_units,
    use_half_of_day = twelveHourTime,

    # Location Data
    location_name = location_data["name"],
    location_state = location_data["state"],

    # Current Weather Data
    cw_icon = curr_weather_data['icon'],
    cw_icon_alt = curr_weather_data["alt_text"],
    curr_temp = curr_weather_data["temp"],
    curr_description = curr_weather_data['description'],

    # Sun Data
    sun_rise_exists = sun_data["rise_exists"],
    sun_rise_time = sun_data["rise"],
    sun_rise_half_of_day = sun_data["rise_half"],

    sun_set_exists = sun_data["set_exists"],
    sun_set_time = sun_data["set"],
    sun_set_half_of_day = sun_data["set_half"],

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
    aqi = aqi_data,

    # Hourly Data
    hourly_template_data = hourly_data,

    # Daily Data
    daily_template_data = daily_data,
)

with open("weather.html", "w") as html:
    html.write(output)

print('Process completed successfully')
