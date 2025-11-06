# Developer Mode
dev_mode = False # ! True = developer mode output | False (default) = no developer mode output

# Screen Size
screen = {
    # This program is developed to support resolutions between 800x480 - 1920x1080
    'width': 1920, # ! Change this value to modify screenshot width (default: 1920)
    'height': 1080, # ! Change this value to modify screenshot height (default: 1080)
}

# Temperature Units
temp_units = ['standard', 'metric', 'imperial'] # Kelvin, Celcius, Fahrenheit
config_temp_units = temp_units[2] # ! Change this index value to change which units of measurement you use (default: imperial)

# Speed Units
speed_units = ['standard', 'imperial']
config_speed_units = speed_units[1] # ! Change this index value to change which units of speed you use (default: imperial)

# Use 12 hour clock or 24 hour clock
twelve_hour_time = True # ! True (default) = use 12 hour clock | False = use 24 hour clock

# API Language
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
language = supported_langs[14] # ! Change this index value to select your preferred language for API requests (Note: will not change any hard-coded text in the HTML)

# Use Geocoding API
# Note: Technically the Geocoding API does not need to be used, but you will have to manually set your location values in the fields provided here:
geocode = {
  'use_api': True, # ! KEEP AS TRUE IF YOU WISH TO CONTRIBUTE CODE TO THIS PROJECT
  'location_name': '', # ! DO NOT FILL IF YOU WISH TO CONTRIBUTE CODE TO THIS PROJECT
  'location_state': '', # ! DO NOT FILL IF YOU WISH TO CONTRIBUTE CODE TO THIS PROJECT
}

