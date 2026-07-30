# Weather Dashboard

### SkyCast

SkyCast is a weather forecasting web application built with **Flask**
and **SQLite**. It allows users to search for any city and view its
current weather conditions along with a 5-day forecast. The application
also keeps a history of recent searches and lets users save their
favorite cities for quick access.

------------------------------------------------------------------------

## Features

-   **Current Weather**: Displays the current temperature, humidity,
    wind speed, and weather description for any searched city.
-   **5-Day Forecast**: Provides a five-day weather forecast with daily
    minimum and maximum temperatures.
-   **Search History**: Automatically stores recent weather searches
    using SQLite.
-   **Favorite Cities**: Save and manage favorite cities for quick
    access.
-   **Temperature Unit Toggle**: Switch between Celsius (°C) and
    Fahrenheit (°F).
-   **Dynamic Backgrounds**: Background theme changes according to the
    current weather condition.

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Flask
-   SQLite
-   HTML5
-   CSS3
-   JavaScript
-   Open-Meteo Geocoding API
-   Open-Meteo Forecast API

------------------------------------------------------------------------

## Project Structure

``` text
weather_dashboard/

    app.py                 # Main Flask application and routes
    database.py            # SQLite database functions
    weather.db             # SQLite database (generated automatically)

    templates/
        home.html          # Home page
        weather.html       # Weather page
    
    static/
        style.css          # Application stylesheet

    README.md
```

------------------------------------------------------------------------

## Installation

### Prerequisites

-   Python 3.x
-   Flask
-   Requests

### Install Dependencies

``` bash
pip install flask requests
```

### Run the Application

``` bash
python app.py
```

Then open:

``` text
http://127.0.0.1:5000/
```

The SQLite database (`weather.db`) will be created automatically when
the application starts.

------------------------------------------------------------------------

## Database

The application uses SQLite with two tables:

### searches

Stores users' recent weather searches.

-   City
-   Temperature
-   Humidity
-   Wind Speed
-   Weather Description
-   Search Timestamp

### favorites

Stores users' favorite cities.

-   City
-   Country
-   Date Added

------------------------------------------------------------------------

## Application Workflow

1.  Search for a city.
2.  The application retrieves its coordinates using the Open-Meteo
    Geocoding API.
3.  Weather data and a 5-day forecast are requested from the Open-Meteo
    Forecast API.
4.  The search is saved in the SQLite database.
5.  Users can add or remove favorite cities.
6.  Search history and favorites are displayed on the home page.

------------------------------------------------------------------------

## Future Improvements

-   Hourly weather forecast
-   Weather charts
-   GPS location support
-   Dark mode
-   User accounts




