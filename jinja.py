from config import (
    config_speed_units, 
    config_temp_units, 
    dev_mode, 
    geocode,
    language,
    twelve_hour_time, 
)
from datetime import datetime
from dotenv import load_dotenv
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from os import getenv
from requests import get

####################
# Functions & Data #
####################

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

weekday = (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
)

month = (
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
)

#################
# Env Variables #
#################
load_dotenv()

API_KEY = getenv('API_KEY')
LATITUDE = getenv('LATITUDE')
LONGITUDE = getenv('LONGITUDE')

##############
# Set Config #
##############

disp_temp_units = None
match config_temp_units:
    case 'standard': disp_temp_units = 'K'
    case 'metric': disp_temp_units = 'C'
    case 'imperial': disp_temp_units = 'F'
    case _: disp_temp_units = 'K'

s_units = config_speed_units
match s_units:
    case 'standard': s_units = 'm/s'
    case 'imperial': s_units = 'mph'
    case _: s_units = 'm/s'

mm_to_inch = 0.03937008  # 1mm = 0.03937008 inch

#####################
# One Call API Data #
#####################

one_call_api: str = f'https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,alerts&units={config_temp_units}&lang={language}&appid={API_KEY}'
# https://openweathermap.org/api/one-call-3#parameter

curr_date = {
    'weekday': None,
    'month': None,
    'day': None,
}

sun_data = {
    'rise': None,
    'rise_half': None,

    'set': None,
    'set_half': None,
}

moon_data = {
    'rise': None,
    'rise_half': None,

    'set': None,
    'set_half': None,
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

r_one_call_data = get(one_call_api)

if (r_one_call_data.status_code == 200):
    one_call_json = r_one_call_data.json()
    
    # Current Date
    converted_date = datetime.fromtimestamp(one_call_json['current']['dt'])
    curr_date['weekday'] = weekday[converted_date.isoweekday() - 1]
    curr_date['month'] = month[converted_date.month - 1]
    curr_date['day'] = converted_date.day

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
            rise_dt = datetime.fromtimestamp(sun_data['rise'])
            rise_hour = rise_dt.hour
            rise_min = rise_dt.minute

            if (twelve_hour_time):
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
            set_dt = datetime.fromtimestamp(sun_data['set'])
            set_hour = set_dt.hour
            set_minute = set_dt.minute

            if (twelve_hour_time):
                set_hour, sun_data['set_half'] = find_half_of_day(set_hour)
                sun_data['set'] = f'{set_hour}:{set_minute:02d}'
            else:
                sun_data['set'] = f'{set_hour:02d}:{set_minute:02d}'
    except:
        if (dev_mode):
            print('Could not find sun set for current weather')

    # Moon Data
    try:
        moon_data['rise'] = one_call_json['daily'][0]['moonrise']

        if (moon_data['rise'] != None):
            mrise_dt = datetime.fromtimestamp(moon_data['rise'])
            mrise_hour = mrise_dt.hour
            mrise_min = mrise_dt.minute

            if (twelve_hour_time):
                mrise_hour, moon_data['rise_half'] = find_half_of_day(mrise_hour)
                moon_data['rise'] = f'{mrise_hour}:{mrise_min:02d}'
            else:
                moon_data['rise'] = f'{mrise_hour:02d}:{mrise_min:02d}'
    except:
        if (dev_mode):
            print('Could not find moon rise data for daily weather index 0')

    try:
        moon_data['set'] = one_call_json['daily'][0]['moonset']

        if (moon_data['set'] != None):
            mset_dt = datetime.fromtimestamp(moon_data['set'])
            mset_hour = mset_dt.hour
            mset_min = mset_dt.minute

            if (twelve_hour_time):
                mset_hour, moon_data['set_half'] = find_half_of_day(mset_hour)
                moon_data['set'] = f'{mset_hour}:{mset_min:02d}'
            else:
                moon_data['set'] = f'{mset_hour:02d}:{mset_min:02d}'
    except:
        if (dev_mode):
            print('Could not find moon set data for daily weather index 0')

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
    visibility_data['distance'] = round(one_call_json['current']['visibility'] * 0.001, 2)

    if (visibility_data['distance'] == 10.00):
        visibility_data['symbol'] = '>'

    # Pressure
    pressure_data = one_call_json['current']['pressure']

    # Ultra-Violet Index
    uvi_data = one_call_json['current']['uvi']

    # Dew Point Data
    dew_point_data = round(one_call_json['current']['dew_point'])

    # Cloud Data
    cloud_data = one_call_json['current']['clouds']

    # Hourly Data
    for i in range(12):
        x = i + 1  # Index for json, 0 = current hour
        
        hourly_data.append(
            {
                'index': i,
                'time': None,
                'half_of_day': None,
                'prob_of_precip': round(one_call_json['hourly'][x]['pop'] * 100),
                'temp': round(one_call_json['hourly'][x]['temp']),
                'rain_vol': None,
                'rain_units': 'mm/h',
                'snow_vol': None,
                'snow_units': 'mm/h',
            }
        )

        # Time
        hourly_data[i]['time'] = one_call_json['hourly'][x]['dt']
        hourly_time = datetime.fromtimestamp(hourly_data[i]['time'])
        hour = hourly_time.hour

        if (twelve_hour_time):
            hour, hourly_data[i]['half_of_day'] = find_half_of_day(hour)
            hourly_data[i]['time'] = f'{hour}'
        else:
            hourly_data[i]['time'] = f'{hour:02d}'

        # Rain & Snow Data
        try:
            hourly_data[i]['rain_vol'] = one_call_json['hourly'][x]['rain']['1h']
        except:
            # print('Could not find rain data')
            if (dev_mode):
                print(
                    f'No hourly rain data for json index: {x} | array index: {i}')

        try:
            hourly_data[i]['snow_vol'] = one_call_json['hourly'][x]['snow']['1h']
        except:
            if (dev_mode):
                print(
                    f'No hourly snow data for json index: {x} | array index: {i}')

        if (config_temp_units == 'imperial' and (hourly_data[i]['rain_vol'] != None or hourly_data[i]['snow_vol'] != None)):
            if (hourly_data[i]['rain_vol'] != None):
                hourly_data[i]['rain_vol'] *= mm_to_inch
                hourly_data[i]['rain_units'] = 'in/h'

            if (hourly_data[i]['snow_vol'] != None):
                hourly_data[i]['snow_vol'] *= mm_to_inch
                hourly_data[i]['snow_units'] = 'in/h'

    hourly_temp_values = [item['temp'] for item in hourly_data]
    hourly_pop_values = [item['prob_of_precip'] for item in hourly_data]
    hourly_data_labels = []

    for i in hourly_data:
        if (twelve_hour_time):
            hourly_data_labels.append(f"{i['time']} {i['half_of_day']}")
        else:
            hourly_data_labels.append(i['time'])


    # Daily Data
    for i in range(4):
        x = i + 1  # index for json, 0 = current day
        
        daily_data.append(
            {
                'index': i,
                
                'date': None,

                'low_temp': round(one_call_json['daily'][x]['temp']['min']),
                'high_temp': round(one_call_json['daily'][x]['temp']['max']),

                'sun_rise': None,
                'sun_rise_half_of_day': None,

                'sun_set': None,
                'sun_set_half_of_day': None,

                'moon_rise': None,
                'moon_rise_half_of_day': None,

                'moon_set': None,
                'moon_set_half_of_day': None,

                'prob_of_precip': round(one_call_json['daily'][x]['pop'] * 100),

                'rain_vol': None,
                'rain_units': 'mm.',

                'snow_vol': None,
                'snow_units': 'mm.',

                'icon': one_call_json['daily'][x]['weather'][0]['icon'],
                'alt_text': None,
            }
        )

        # Date
        daily_data[i]['date'] = one_call_json['daily'][x]['dt']
        daily_date_dt = datetime.fromtimestamp(daily_data[i]['date'])
        daily_month = month[daily_date_dt.month - 1]

        daily_day = daily_date_dt.day

        daily_date = weekday[daily_date_dt.isoweekday() - 1]

        daily_data[i]['date'] = f'{daily_date}, {daily_month} {daily_day}'

        # Sun Rise
        try:
            daily_data[i]['sun_rise'] = one_call_json['daily'][x]['sunrise']

            if (daily_data[i]['sun_rise'] != None):
                daily_dt_s_rise = datetime.fromtimestamp(daily_data[i]['sun_rise'])
                daily_srh = daily_dt_s_rise.hour
                daily_srm = daily_dt_s_rise.minute

                if (twelve_hour_time):
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
                daily_dt_s_set = datetime.fromtimestamp(daily_data[i]['sun_set'])
                daily_ssh = daily_dt_s_set.hour
                daily_ssm = daily_dt_s_set.minute

                if (twelve_hour_time):
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
                daily_dt_m_rise = datetime.fromtimestamp(daily_data[i]['moon_rise'])
                daily_mrh = daily_dt_m_rise.hour
                daily_mrm = daily_dt_m_rise.minute

                if (twelve_hour_time):
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
                daily_dt_m_set = datetime.fromtimestamp(daily_data[i]['moon_set'])
                daily_msh = daily_dt_m_set.hour
                daily_msm = daily_dt_m_set.minute

                if (twelve_hour_time):
                    daily_msh, daily_data[i]['moon_set_half_of_day'] = find_half_of_day(daily_msh)
                    daily_data[i]['moon_set'] = f'{daily_msh}:{daily_msh:02d}'
                else:
                    daily_data[i]['moon_set'] = f'{daily_msh:02d}:{daily_msh:02d}'
        except:
            if (dev_mode):
                print('Cannot find daily moon set')

        # Rain & Snow
        try:
            daily_data[i]['rain_vol'] = one_call_json['daily'][x]['rain']
        except:
            if (dev_mode):
                print(f'No daily rain data for json index: {x} | array index: {i}')

        try:
            daily_data[i]['snow_vol'] = one_call_json['daily'][x]['snow']
        except:
            if (dev_mode):
                print(f'No daily snow data for json index: {x} | array index: {i}')

        if (config_temp_units == 'imperial'):
            if (daily_data[i]['rain_vol'] != None):
                daily_data[i]['rain_vol'] = round(daily_data[i]['rain_vol'] * mm_to_inch, 2)

            daily_data[i]['rain_units'] = 'in.'

            if (daily_data[i]['snow_vol'] != None):
                daily_data[i]['snow_vol'] = round(daily_data[i]['snow_vol'] * mm_to_inch, 2)

            daily_data[i]['snow_units'] = 'in.'

        # Alt Text
        daily_data[i]['alt_icon'] = set_alt_text(daily_data[i]['icon'])

else:
    print(f'Could not get One Call API data: {r_one_call_data.status_code}')

########################
# Air Quality Index Data
########################

air_quality_api: str = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}'
aqi_data = None

r_air_quality_data = get(air_quality_api)

if (r_air_quality_data.status_code == 200):
    quality_list = ('Good', 'Fair', 'Moderate', 'Poor', 'Very Poor')
    
    air_quality_json = r_air_quality_data.json()

    aqi_data = quality_list[air_quality_json['list'][0]['main']['aqi'] - 1]
else:
    print(
        f'Could not get Air Quality API data: {r_air_quality_data.status_code}')

####################
# Geocoding API Data
####################
location_data = {
    'name': None,
    'country': None,
    'state': None,
}

if (geocode['use_api']):
    geocoding_api: str = f'http://api.openweathermap.org/geo/1.0/reverse?lat={LATITUDE}&lon={LONGITUDE}&limit=1&appid={API_KEY}'

    r_geocoding_data = get(geocoding_api)

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
    use_half_of_day = twelve_hour_time,

    # Location Data
    geocode_local = geocode,
    location = location_data,

    # Current Date
    date = curr_date,

    # Current Weather Data
    current = curr_weather_data,

    # Sun Data
    sun = sun_data,

    # Moon Data
    moon = moon_data,

    # Wind Speed Data
    wind = wind_data,

    # Humidity Data
    humidity = humidity_data,

    # Visibility Data
    visibility = visibility_data,

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
    chart_temp_dataset = hourly_temp_values,
    chart_pop_dataset = hourly_pop_values,
    chart_labels = hourly_data_labels,

    # Daily Data
    daily_template_data = daily_data,
)

with open("weather.html", "w") as html:
    html.write(output)

print('Process completed successfully')
