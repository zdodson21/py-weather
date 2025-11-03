# Py-Weather

Beginner friendly weather dashboard designed for Raspberry Pi computers paired with an external display.

**Note: While this code is documented to make changing it as simple as possible,
it is still assumed that you have at least a basic understanding of Python to be
able to read and understand the code written here in order to configure this program
for your personal use.**

**For modifiable values, search for the string `[modifiable]` in the `jinja.py` file.**

## Setup / Commands

```bash
# Ensure you have the latest updates

git pull
```

### Required Packages

#### Firefox (should come pre-installed on Raspberry Pi OS)

```bash
# Test if Firefox is installed
firefox --version

# Output should look something like this (version number shouldn't* matter):
# `Mozilla Firefox 142.0.1`

# If you get a response saying something like 'firefox: command not found', run the following command to install it:
sudo apt install firefox
```

#### Will add image viewer here when I better understand it

### Install Python  Dependencies

Two options exist to install dependencies. [Pip](https://docs.python.org/3/installing/index.html),
which is included with Python, and [Pipenv](https://pipenv.pypa.io/en/latest/), which is a separate install.

- Use `pip` if you are a beginner with Python & Raspberry Pi / Linux
- Use `pipenv` if you are a more advanced user of Python & Raspberry Pi / Linux.

#### Using Pip

```bash
# Set up .venv
python -m venv .venv
```

```bash
# Enter virtual environment 
source .venv/bin/activate
```

```bash
# Install packages
pip install requests jinja2 python-dotenv playwright
```

```bash
# Install playwright
playwright install
```

#### Using Pipenv

[Pipenv Install](https://packaging.python.org/en/latest/tutorials/managing-dependencies/)

Run the following commands from root project directory to setup project:

```bash
# Ensure virtual environment is created within project root directory

# You can either run this command every time you use this project or place it in your `.bashrc` / `.zshenv`

export PIPENV_VENV_IN_PROJECT=1
```

```bash
# Install dependencies
pipenv install
```

```bash
# Enter virtual environment
pipenv shell
```

```bash
# Install playwright
playwright install
```

#### Running the Project

```bash
# Run Jinja Python Script (must be in virtual environment)
python jinja.py
```

**Optional: The following command is not required to use this project. CSS will be updated before `git push`,
so you do not have to build it yourself. The following is provided in case I forget to provide updated CSS
or you wish to compile the CSS file yourself.**

```bash
# Install Sass (Node.Js Required)
npm install -g sass

# Compile .sass to .css
sass styles/style.sass styles/style.css
```

### Environment Variables

Included is a file named `.sample.env`. This file is prepopulated with all environment variables set to blank values.
For this project to run you must complete the following:

1. Obtain an API key from [OpenWeather](https://openweathermap.org/api)
   - Note: The code for this program is written to stay well below the "1,000 API calls per day for free",
     however I am not responsible for any charges that may occur for use of this API in conjunction with this code.
     You should audit / test this code yourself to ensure you will not exceed the API call limit, especially if you modify it for your needs.
   - This project uses the following APIs:
     - [One Call](https://openweathermap.org/api/one-call-3)
     - [Geocoding](https://openweathermap.org/api/geocoding-api)
     - [Air Pollution](https://openweathermap.org/api/air-pollution)

1. Populate the environment variables with your API key & coordinates. You are responsible for finding the coordinates you wish to use.

1. Remove the comments from the top of `.sample.env`

1. Rename `.sample.env` to `.env`

You should now be able to properly populate an html file from the `template.html` file by running the `python jinja.py` command.

## Managing the Process

### Starting It

You can either run the following command natively in your Raspberry Pi's terminal, or you can connect to it via ssh.
Just ensure you run the following command from the root directory of this project while in your Python virtual environment.

```bash
# Start the program (if this does not work, then try `source`)
bash run.sh
```

### Killing It

To kill the process, run the following command:

```bash

```

---

## Some Weather Terms Explained

**Note:** These explanations are not written by a meteorologist.
They are intended to be an introduction to each term.
If you wish to learn more about any of the terms below, you are encouraged to research them using scientific books and websites.

### Temperature

Temperature is the measure of the kinetic energy of the vibrating atoms of matter.

#### Units of Measurement

- **Kelvin**: Thermodynamic temperature measurement unit starting at the lowest possible temperature of 0 K (absolute zero).
  - **Absolute Zero**: The lowest possible temperature in which any atoms of a substance cease to vibrate.
- **Celsius**: Temperature system where the freezing point of water = 0&deg; and the boiling point of water = 100&deg;.
- **Fahrenheit**: Temperature system where the freezing point of water = 32&deg; and the boiling point of water = 212&deg;.

### Wind

- **Direction**: The direction the wind is coming from / traveling in.
- **Speed**: Speed in which the wind is traveling.
- **Gust**: A sudden increase in wind speed.

### Humidity

- **Definition**: Concentration of water vapor present in the air, indicating the likelihood for precipitation, dew, and/or fog to be present.
- **What does 100% humidity mean?**: 100% humidity means the air is holding the maximum amount of water it can at its current temperature.

### Visibility

- **Definition**: How far a healthy human eye can see factoring in meteorological obstacles such as fog, clouds, and more.

### Barometric Pressure

- **Definition**: Force exerted by the body of air above an area.
- **How is it measured?**: A mercury barometer can be used, with the height of the mercury in the barometer changing with the
                           barometric pressure surrounding it. It is measured in pascal units (Pa), with 1 Pa = N/m^2 (1 newton (N) = 1 kg * m/s^2).
- **What is `hPa`?**: hPa stands for hectopascal (1 hPa = 100 Pa)

### Ultra Violet Index (UVI)

- **Definition**: Measurement of the intensity of ultra-violet radiation. Higher UVI results in increased risk of sunburn.

### Air Quality

- **Definition**: Measurement of how polluted the air is at a given time.

### Dew Point

- **Definition**: The temperature air has to be cools to for the relative humidity to be 100%.

### Cloud Coverage

- **Definition**: Volume of the sky covered by clouds, measured as a percentage.

### Moon Phases

Moon phases are caused by the Moon's position in Earth's orbit and how much light is shone on the visible surface of the moon. The below image by Nasa does a good job visualizing what causes the phases of the Moon.
![Image by NASA](https://spaceplace.nasa.gov/review/moon-phases/moon-phases.en.png)
[You can learn more about the Moon phases on this Nasa website.](https://spaceplace.nasa.gov/moon-phases/en/)

## Other Information

- [Project Repository](https://github.com/zdodson21/py-weather)
- [License](https://github.com/zdodson21/py-weather/blob/main/LICENSE)
- [OpenWeather](https://openweathermap.org/)
- [Project Inspiration](https://youtu.be/65sda565l9Y?si=k6-RwbBIYO7BNilD)
