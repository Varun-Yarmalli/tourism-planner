 Tourism-Planner System

This project is a fast and intelligent multi-agent system designed to help users plan their trips by providing real-time weather information and curated tourist attraction suggestions for any city around the world.

Features

Fast response times through parallel processing and intelligent caching

Works regardless of capitalization

Handles minor spelling mistakes

Supports cities worldwide

Provides current temperature and precipitation probability

Suggests up to five tourist attractions

Robust error handling to manage incorrect or unknown locations

Natural language understanding for flexible query formats

Uses open-source APIs, so no API keys are required

Architecture Overview

Tourism AI Agent (tourism_agent.py): The parent agent that coordinates the entire workflow

Weather Agent (weather_agent.py): A child agent that retrieves weather data from the Open-Meteo API

Places Agent (places_agent.py): A child agent that retrieves tourist attraction data from the Overpass API

APIs Used

Open-Meteo API for weather forecasting

Nominatim API for geocoding (converting place names to coordinates)

Overpass API for retrieving tourist attractions from OpenStreetMap data

Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/tourism-planner
cd tourism-planner


Install the required dependencies:

pip install -r requirements.txt

Usage
Running Locally

Start the Flask server:

python app.py


Then open the browser at:
http://localhost:5000

Command Line Interface

Run the CLI mode:

python main.py

Example Queries

I am going to Bangalore, let's plan my trip.

I am going to Bangalore, what is the temperature there.

I am going to Bangalore, what is the temperature and what places can I visit.

System Workflow

The user enters a query that contains a place name.

The parent agent identifies the place and determines whether the user wants weather information, tourist places, or both.

The system uses the Nominatim API to convert the place name into coordinates and verify that the location exists.

If the place is invalid, the system returns a clear error message.

If weather information is needed, the Weather Agent fetches it from Open-Meteo.

If tourist attractions are needed, the Places Agent retrieves them from the Overpass API.

The parent agent combines and formats the output before returning it to the user.

Deployment Options
Heroku

Install the Heroku CLI

Run heroku login

Create an app and push your code

Railway

Connect the repository to Railway

Railway automatically detects the environment and deploys

Render

Connect the repository to Render

Select Web Service

Use the standard Python build and start commands

Performance Improvements

Weather and place data are fetched in parallel

Coordinates are cached to speed up repeated queries

API calls are optimized to reduce response time

Fuzzy matching is used to handle spelling errors

Error Handling

Unknown locations generate a clear and friendly error

API failures are handled gracefully

Users are prompted for valid inputs when needed

Contributing

Contributions, suggestions, and feature requests are welcome.
