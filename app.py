from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from database import ( init_db, save_search, get_history, clear_all_history, add_favorite, remove_favorite, get_favorites, is_favorite )

app = Flask(__name__)
app.secret_key = "my-weather-app-2026"  
init_db()


# maps World Meteorological Organization weather codes to descriptions and icons
WEATHER_DESCRIPTIONS = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌧️"),
    57: ("Dense freezing drizzle", "🌧️"),
    61: ("Slight rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌨️"),
    67: ("Heavy freezing rain", "🌨️"),
    71: ("Slight snow fall", "🌨️"),
    73: ("Moderate snow fall", "🌨️"),
    75: ("Heavy snow fall", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with slight hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
}

# Groups codes into a theme name used to change the page background
CATEGORY_MAP = {
    "clear": {0},
    "cloudy": {1, 2, 3},
    "fog": {45, 48},
    "rain": {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82},
    "snow": {71, 73, 75, 77, 85, 86},
    "thunderstorm": {95, 96, 99},
}



def describe_weather(code):   # returns a tuple of (description, icon) for a given weather code. 
    return WEATHER_DESCRIPTIONS.get(code, ("Unknown", "❓"))


def weather_category(code):
    for category, codes in CATEGORY_MAP.items():
        if code in codes:
            return category
    return "default"


def get_coordinates(city): # converts a city name into latitude and longitude coordinates using Open-Meteo Geocoding API.
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    res = requests.get(url).json()
    if "results" not in res:
        return None
    result = res["results"][0]
    return result["latitude"], result["longitude"], result["name"], result.get("country", "")


def get_weather(lat, lon): # fetches current weather and 5-day forecast for given latitude and longitude.
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,weather_code"
        "&timezone=auto"
    )
    return requests.get(url).json()


# Fetches weather data for a given city.
def fetch_weather_data(city):

    coords = get_coordinates(city)
    if coords is None:
        return None

    lat, lon, city_name, country = coords
    data = get_weather(lat, lon)
    current = data["current"]
    desc, icon = describe_weather(current["weather_code"])
    category = weather_category(current["weather_code"])

    # 5-day forecast list
    forecast = []
    daily = data["daily"]
    for i in range(min(5, len(daily["time"]))):
        f_desc, f_icon = describe_weather(daily["weather_code"][i])
        forecast.append({
            "date": daily["time"][i],
            "max": daily["temperature_2m_max"][i],
            "min": daily["temperature_2m_min"][i],
            "desc": f_desc,
            "icon": f_icon,
        })

    return {
        "city": city_name,
        "country": country,
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "windspeed": current["wind_speed_10m"],
        "description": desc,
        "icon": icon,
        "category": category,
        "forecast": forecast,
    }



#home page displays search history and favorite cities. 
@app.route("/")
def home():
    history = get_history()
    favorites = get_favorites()
    return render_template("home.html", history=history, favorites=favorites)


# weather page displays current weather and 5-day forecast for a given city.
@app.route("/weather")
def weather_page():
    city = request.args.get("city", "").strip()
    if not city:
        flash("Please enter a city name.", "error")
        return redirect(url_for("home"))

    weather = fetch_weather_data(city)
    if weather is None:
        flash(f'City "{city}" not found. Try again.', "error")
        return redirect(url_for("home"))

    save_search(
        weather["city"],
        weather["temperature"],
        weather["humidity"],
        weather["windspeed"],
        weather["description"],
    )

    weather["is_favorite"] = is_favorite(weather["city"])
    return render_template("weather.html", weather=weather)


@app.route("/clear-history", methods=["POST"])
def clear_history():
    clear_all_history()
    flash("History cleared.", "success")
    return redirect(url_for("home"))


@app.route("/favorite/add", methods=["POST"])
def favorite_add():
    city = request.form.get("city")
    country = request.form.get("country", "")
    if city:
        add_favorite(city, country)
        flash(f'{city} added to favorites!', "success")
    return redirect(url_for("weather_page", city=city))


@app.route("/favorite/remove", methods=["POST"])
def favorite_remove():
    city = request.form.get("city")
    redirect_to = request.form.get("redirect_to", "home")
    if city:
        remove_favorite(city)
        flash(f'{city} removed from favorites.', "success")
    if redirect_to == "weather":
        return redirect(url_for("weather_page", city=city))
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)