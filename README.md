# Py-Weather

Weather dashboard designed for Raspberry Pi computers paired with an external display.

**Note: While this code is documented to make changing it as simple as possible, it is still assumed that you have at least a basic understanding of Python to be able to read and understand the code written here in order to configure this program for your personal use.**

**For modifiable values, search for the string `[modifiable]` in the `jinja.py` file.**

## Setup / Commands

### Install Dependencies

[Pipenv is used to install dependencies](https://packaging.python.org/en/latest/tutorials/managing-dependencies/)

Run the following commands from root project directory to setup project:

```bash
# Ensure virutal environment is created within project root directory

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

#### If You Can't Use `pipenv`

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

pip install requests jinja2 python-dotenv
```

```bash
# Run Jinja Python Script (must be in virtual environment)

python jinja.py
```

**Optional: The following command is not required to use this project. CSS will be updated before `git push`, so you do not have to build it yourself. The following is provided in case I forgot to provide updated CSS or you wish to compile the CSS file yourself.**

```bash
# Install Sass (Node.Js Required)
npm install -g sass

# Compile .sass to .css
sass styles/style.sass styles/style.css
```

### Environment Variables

Included is a file named `.sample.env`. This file is prepopulated with all environment variables set to blank values. For this project to run you must complete the following:

1. Obtain an API key from [OpenWeather](https://openweathermap.org/api)
   - Note: The code for this program is written to stay well below the "1,000 API calls per day for free", however I am not responsible for any charges that may occur for use of this API in conjunction with this code. You should audit / test this code yourself to ensure you will not exceed the API call limit, especially if you modify it for your needs.
   - This project uses the following APIs:
     - [One Call](https://openweathermap.org/api/one-call-3)
     - [Geocoding](https://openweathermap.org/api/geocoding-api)
     - [Air Pollution](https://openweathermap.org/api/air-pollution)

2. Populate the environment variables with your API key & coordinates. You are responsible for finding the coordinates you wish to use.

3. Remove the comments from the top of `.sample.env`

4. Rename `.sample.env` to `.env`

You should now be able to properly populate an html file from the `template.html` file by running the `python jinja.py` command.

## What does all the weather lingo mean?

**Note: not written by a weather expert.**


