import requests
import matplotlib.pyplot as plt
import streamlit as st
import datetime

API_KEY = "69fc5c5baeb423ac0f0d33ba2e193c21"

weather_now_url = "http://api.openweathermap.org/data/2.5/weather"
weekly_weather_url = "https://api.openweathermap.org/data/2.5/onecall"

LANGUAGES = {
    "עברית": "he",
    "English": "en"
}

TEXTS = {
    "עברית": {
        "title": "🌦 מה מזג האוויר?",
        "enter_city": "🏙️ בחר/י את העיר הרצויה:",
        "show_forecast": "📈 הצג תחזית",
        "current_weather": "מזג האוויר כעת ב",
        "temp": "🌡 טמפרטורה:",
        "humidity": "💧 לחות:",
        "description": "☁ עננות:",
        "weekly_forecast": "📊 תחזית ל-7 ימים הקרובים עבור",
        "no_city": "❗ הקלד/י שם עיר כדי להציג תחזית.",
        "fetch_error": "שגיאה! יש לבדוק את הנתונים שהוזנו"
    },
    "English": {
        "title": "🌦 What Is The Weather?",
        "enter_city": "🏙️ Enter a city:",
        "show_forecast": "📈 Show Forecast",
        "current_weather": "Current weather in",
        "temp": "🌡 Temperature:",
        "humidity": "💧 Humidity:",
        "description": "☁ Cloudiness:",
        "weekly_forecast": "📊 7-Day Forecast for",
        "no_city": "❗ Please enter a city name to show forecast.",
        "fetch_error": "❌ Could not fetch data. Check city name or API Key."
    }
}

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        right: 0;
        left: auto;
    }
    section[data-testid="stSidebar"] > div:first-child {
        width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

language_choice = st.sidebar.radio("🌍 עברית / English", options=list(LANGUAGES.keys()))
language = LANGUAGES[language_choice]
text = TEXTS[language_choice]

if language_choice == "עברית":
    st.markdown("<style>body {direction: rtl; text-align: right;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body {direction: ltr; text-align: left;}</style>", unsafe_allow_html=True)

st.title(text["title"])
city = st.text_input(text["enter_city"])

def weather_now(city, language):
    now_url = f"{weather_now_url}?q={city}&appid={API_KEY}&units=metric&lang={language}"
    response = requests.get(now_url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        st.subheader(f"{text['current_weather']} {city_name}:")
        st.write(f"{text['temp']} {temp}°C")
        st.write(f"{text['humidity']} {humidity}%")
        st.write(f"{text['description']} {description}")
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        st.error(text["fetch_error"])
        return None, None

def weekly_weather(lat, lon, city, language):
    weekly_url = f"{weekly_weather_url}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang={language}&exclude=current,minutely,hourly,alerts"
    response = requests.get(weekly_url)
    if response.status_code == 200:
        forecast_data = response.json()
        days = []
        temps = []
        for i, day in enumerate(forecast_data["daily"][:7]):  # עכשיו 7 ימים
            temp_day = day["temp"]["day"]
            temps.append(temp_day)
            days.append(datetime.datetime.fromtimestamp(day["dt"]).strftime("%d/%m"))
        st.subheader(f"{text['weekly_forecast']} {city}")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(days, temps, marker="o", linestyle="solid")
        ax.set_xlabel("")
        ax.set_ylabel("°C", fontsize=12)
        ax.tick_params(axis='x', labelrotation=45)
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error(text["fetch_error"])

if st.button(text["show_forecast"]):
    if city:
        lat, lon = weather_now(city, language)
        if lat and lon:
            weekly_weather(lat, lon, city, language)
    else:
        st.warning(text["no_city"])
